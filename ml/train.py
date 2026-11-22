"""
LearnCraft AI - Milestone 3 training script.

Trains and compares statistical ML models that predict how hard a passage is
to read, using the CommonLit Ease of Readability (CLEAR) corpus.

    Target (regression):      BT_easiness  (higher = easier, teacher-rated)
    Target (classification):  Hard / Medium / Easy  (tertiles of BT_easiness)

Run from the project root:
    python ml/train.py

Outputs:
    results/metrics.json            all numbers quoted in the report
    results/*.csv                   comparison tables
    results/figures/*.png           every figure in the report
    models/best_regressor.joblib    best overall model (sklearn pipeline)
    models/ridge_features.json      light model exported for the Node backend
"""
import json
import os
import sys
import time
import warnings

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.sparse import hstack, csr_matrix
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import (accuracy_score, adjusted_rand_score, classification_report,
                             confusion_matrix, f1_score, mean_absolute_error,
                             mean_squared_error, r2_score)
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score, learning_curve, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.svm import SVR, LinearSVC
from sklearn.tree import DecisionTreeRegressor

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ml"))
from features import (FEATURE_NAMES, COMMON_WORDS, HandFeatures, down_weight_sparse,  # noqa: E402
                      feature_frame, select_fkgl)

SEED = 42
DATA = os.path.join(ROOT, "dataset", "clear_corpus.csv")
RES = os.path.join(ROOT, "results")
FIG = os.path.join(RES, "figures")
MOD = os.path.join(ROOT, "models")
for d in (RES, FIG, MOD):
    os.makedirs(d, exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook")
PALETTE = ["#2E5A88", "#D9822B", "#3A8D5C", "#B5403A", "#7A5BA6", "#8C8C8C"]
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 160, "font.family": "DejaVu Sans"})


def savefig(name):
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, name), bbox_inches="tight")
    plt.close()


def rmse(y, p):
    return float(np.sqrt(mean_squared_error(y, p)))


def reg_scores(y, p):
    return {"RMSE": rmse(y, p), "MAE": float(mean_absolute_error(y, p)), "R2": float(r2_score(y, p))}


def main():
    t0 = time.time()
    out = {}

    # 1. Load + clean ---------------------------------------------------------
    df = pd.read_csv(DATA)
    n_raw = len(df)
    df = df.dropna(subset=["Excerpt", "BT_easiness"])
    df["Excerpt"] = df["Excerpt"].astype(str).str.strip()
    df = df[df["Excerpt"].str.len() > 50]
    df = df.drop_duplicates(subset="Excerpt").reset_index(drop=True)
    out["data"] = {"rows_raw": n_raw, "rows_clean": len(df),
                   "lit": int((df.Categ == "Lit").sum()), "info": int((df.Categ == "Info").sum())}
    print(f"Loaded {n_raw} rows, {len(df)} after cleaning")

    y = df["BT_easiness"].values
    q1, q2 = np.quantile(y, [1 / 3, 2 / 3])
    labels = np.where(y < q1, "Hard", np.where(y < q2, "Medium", "Easy"))
    df["difficulty"] = labels
    out["data"]["tertile_cuts"] = [float(q1), float(q2)]
    out["data"]["target_stats"] = {k: float(v) for k, v in df["BT_easiness"].describe().items()}

    # 2. Features -------------------------------------------------------------
    X_feat = feature_frame(df["Excerpt"].tolist())
    X_feat.insert(0, "id", df["ID"].values)
    X_feat["BT_easiness"] = y
    X_feat["difficulty"] = labels
    X_feat["category"] = df["Categ"].values
    X_feat.to_csv(os.path.join(ROOT, "dataset", "clear_features.csv"), index=False)
    F = X_feat[FEATURE_NAMES]

    # 3. EDA figures ----------------------------------------------------------
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    sns.histplot(df["BT_easiness"], bins=40, kde=True, color=PALETTE[0], ax=ax[0])
    ax[0].axvline(q1, ls="--", c=PALETTE[3]); ax[0].axvline(q2, ls="--", c=PALETTE[3])
    ax[0].set_title("Distribution of BT_easiness (dashed = class cut-offs)")
    ax[0].set_xlabel("BT_easiness (higher = easier)")
    sns.boxplot(data=df, x="Categ", y="BT_easiness", palette=PALETTE[:2], ax=ax[1])
    ax[1].set_title("Easiness by genre"); ax[1].set_xlabel("")
    ax[1].set_xticklabels(["Literature" if t.get_text() == "Lit" else "Informational" for t in ax[1].get_xticklabels()])
    savefig("01_target_distribution.png")

    corr = F.apply(lambda c: stats.pearsonr(c, y)[0]).sort_values()
    out["feature_correlations"] = {k: float(v) for k, v in corr.items()}
    plt.figure(figsize=(8, 6))
    colors = [PALETTE[3] if v < 0 else PALETTE[2] for v in corr.values]
    plt.barh(corr.index, corr.values, color=colors)
    plt.axvline(0, c="k", lw=0.8)
    plt.title("Pearson correlation of each feature with BT_easiness")
    plt.xlabel("r")
    savefig("02_feature_correlations.png")

    plt.figure(figsize=(10, 8))
    sns.heatmap(F.corr(), cmap="RdBu_r", center=0, square=True, cbar_kws={"shrink": .7},
                xticklabels=True, yticklabels=True)
    plt.title("Feature-feature correlation matrix")
    savefig("03_feature_heatmap.png")

    # 4. Split ----------------------------------------------------------------
    idx_tr, idx_te = train_test_split(np.arange(len(df)), test_size=0.2, random_state=SEED, stratify=labels)
    T_tr, T_te = df["Excerpt"].values[idx_tr], df["Excerpt"].values[idx_te]
    F_tr, F_te = F.values[idx_tr], F.values[idx_te]
    y_tr, y_te = y[idx_tr], y[idx_te]
    lab_tr, lab_te = labels[idx_tr], labels[idx_te]
    out["split"] = {"train": len(idx_tr), "test": len(idx_te)}
    kf = KFold(5, shuffle=True, random_state=SEED)

    # 5. Regression on hand features -----------------------------------------
    fkgl_idx = FEATURE_NAMES.index("flesch_kincaid_grade")
    feat_models = {
        "Mean baseline": DummyRegressor(),
        "FKGL only (linear)": Pipeline([("sel", FunctionTransformer(select_fkgl)),
                                        ("lr", LinearRegression())]),
        "Linear Regression": Pipeline([("sc", StandardScaler()), ("m", LinearRegression())]),
        "Ridge": Pipeline([("sc", StandardScaler()), ("m", Ridge(alpha=1.0))]),
        "Lasso": Pipeline([("sc", StandardScaler()), ("m", Lasso(alpha=0.01))]),
        "Elastic Net": Pipeline([("sc", StandardScaler()), ("m", ElasticNet(alpha=0.01, l1_ratio=0.5))]),
        "KNN (k=15)": Pipeline([("sc", StandardScaler()), ("m", KNeighborsRegressor(15, weights="distance"))]),
        "Decision Tree": DecisionTreeRegressor(max_depth=6, random_state=SEED),
        "SVR (RBF)": Pipeline([("sc", StandardScaler()), ("m", SVR(C=1.0))]),
        "Random Forest": RandomForestRegressor(400, min_samples_leaf=3, n_jobs=-1, random_state=SEED),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=400, learning_rate=0.05, max_depth=3,
                                                       subsample=0.8, random_state=SEED),
    }
    rows, cv_store = [], {}
    for name, m in feat_models.items():
        cv = -cross_val_score(m, F_tr, y_tr, cv=kf, scoring="neg_root_mean_squared_error")
        m.fit(F_tr, y_tr)
        s = reg_scores(y_te, m.predict(F_te))
        cv_store[name] = cv
        rows.append({"Model": name, "Input": "Hand-crafted features", "CV RMSE": cv.mean(), "CV SD": cv.std(), **s})
        print(f"  {name:22s} CV {cv.mean():.3f}  test RMSE {s['RMSE']:.3f} R2 {s['R2']:.3f}")

    # 6. Text models (TF-IDF) -------------------------------------------------
    tfidf_word = lambda: TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=40000, sublinear_tf=True)
    text_models = {
        "TF-IDF words + Ridge": Pipeline([("tf", tfidf_word()), ("m", Ridge(alpha=1.5))]),
        "TF-IDF chars + Ridge": Pipeline([("tf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=3,
                                                                 max_features=60000, sublinear_tf=True)),
                                          ("m", Ridge(alpha=1.5))]),
        "Features + TF-IDF + Ridge": Pipeline([
            ("u", FeatureUnion([
                ("tf", tfidf_word()),
                ("hf", Pipeline([("h", HandFeatures()), ("sc", StandardScaler()),
                                 ("w", FunctionTransformer(down_weight_sparse))])),
            ])),
            ("m", Ridge(alpha=1.5)),
        ]),
    }
    for name, m in text_models.items():
        cv = -cross_val_score(m, T_tr, y_tr, cv=kf, scoring="neg_root_mean_squared_error", n_jobs=-1)
        m.fit(T_tr, y_tr)
        s = reg_scores(y_te, m.predict(T_te))
        cv_store[name] = cv
        rows.append({"Model": name, "Input": "Raw text", "CV RMSE": cv.mean(), "CV SD": cv.std(), **s})
        print(f"  {name:22s} CV {cv.mean():.3f}  test RMSE {s['RMSE']:.3f} R2 {s['R2']:.3f}")

    # 7. Hyper-parameter tuning ----------------------------------------------
    tuned = {}
    gs_ridge = GridSearchCV(text_models["Features + TF-IDF + Ridge"],
                            {"m__alpha": [0.5, 1.0, 1.5, 3.0, 6.0]},
                            cv=kf, scoring="neg_root_mean_squared_error", n_jobs=-1)
    gs_ridge.fit(T_tr, y_tr)
    tuned["Features + TF-IDF + Ridge"] = {"best_params": gs_ridge.best_params_, "cv_rmse": -gs_ridge.best_score_,
                                          "grid": {str(p["m__alpha"]): float(-s) for p, s in
                                                   zip(gs_ridge.cv_results_["params"], gs_ridge.cv_results_["mean_test_score"])}}
    gs_gb = GridSearchCV(GradientBoostingRegressor(subsample=0.8, random_state=SEED),
                         {"n_estimators": [300, 600], "learning_rate": [0.03, 0.06], "max_depth": [2, 3, 4]},
                         cv=kf, scoring="neg_root_mean_squared_error", n_jobs=-1)
    gs_gb.fit(F_tr, y_tr)
    tuned["Gradient Boosting"] = {"best_params": gs_gb.best_params_, "cv_rmse": -gs_gb.best_score_}
    gs_svr = GridSearchCV(Pipeline([("sc", StandardScaler()), ("m", SVR())]),
                          {"m__C": [0.3, 1, 3], "m__gamma": ["scale", 0.02, 0.05], "m__epsilon": [0.1, 0.3]},
                          cv=kf, scoring="neg_root_mean_squared_error", n_jobs=-1)
    gs_svr.fit(F_tr, y_tr)
    tuned["SVR (RBF)"] = {"best_params": gs_svr.best_params_, "cv_rmse": -gs_svr.best_score_}
    for name, gs, Xte, inp in [("Features + TF-IDF + Ridge (tuned)", gs_ridge, T_te, "Raw text"),
                               ("Gradient Boosting (tuned)", gs_gb, F_te, "Hand-crafted features"),
                               ("SVR (tuned)", gs_svr, F_te, "Hand-crafted features")]:
        s = reg_scores(y_te, gs.predict(Xte))
        rows.append({"Model": name, "Input": inp, "CV RMSE": -gs.best_score_, "CV SD": np.nan, **s})
        print(f"  {name:22s} tuned test RMSE {s['RMSE']:.3f} R2 {s['R2']:.3f}")
    out["tuning"] = json.loads(json.dumps(tuned, default=str))

    # 8. Simple ensemble: average of tuned text-ridge and tuned GBR ----------
    p_ens = 0.6 * gs_ridge.predict(T_te) + 0.4 * gs_gb.predict(F_te)
    s = reg_scores(y_te, p_ens)
    rows.append({"Model": "Ensemble (0.6 text Ridge + 0.4 GBR)", "Input": "Both", "CV RMSE": np.nan, "CV SD": np.nan, **s})
    print(f"  Ensemble test RMSE {s['RMSE']:.3f} R2 {s['R2']:.3f}")

    res = pd.DataFrame(rows)
    res.to_csv(os.path.join(RES, "regression_results.csv"), index=False)
    out["regression"] = res.round(4).to_dict(orient="records")

    # Paired t-test on CV folds: best text model vs the classical FKGL formula
    a, b = cv_store["Features + TF-IDF + Ridge"], cv_store["FKGL only (linear)"]
    t, p = stats.ttest_rel(a, b)
    out["ttest_text_vs_fkgl"] = {"t": float(t), "p": float(p), "fold_rmse_text": a.tolist(), "fold_rmse_fkgl": b.tolist()}
    a2 = cv_store["Gradient Boosting"]
    t2, p2 = stats.ttest_rel(a2, b)
    out["ttest_gbr_vs_fkgl"] = {"t": float(t2), "p": float(p2)}

    # Figures: model comparison
    plot_df = res[res["Model"] != "Mean baseline"].sort_values("RMSE")
    plt.figure(figsize=(9, 6))
    cols = [PALETTE[0] if i == "Hand-crafted features" else PALETTE[1] if i == "Raw text" else PALETTE[2]
            for i in plot_df["Input"]]
    plt.barh(plot_df["Model"], plot_df["RMSE"], color=cols)
    base = res.loc[res.Model == "Mean baseline", "RMSE"].iloc[0]
    plt.axvline(base, ls="--", c="k", lw=1)
    plt.text(base, -0.9, " mean baseline", fontsize=8)
    for i, v in enumerate(plot_df["RMSE"]):
        plt.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=8)
    plt.gca().invert_yaxis()
    plt.xlabel("Test RMSE (lower is better)")
    plt.title("Regression models on the held-out test set")
    from matplotlib.patches import Patch
    plt.legend(handles=[Patch(color=PALETTE[0], label="Hand-crafted features"),
                        Patch(color=PALETTE[1], label="Raw text (TF-IDF)"),
                        Patch(color=PALETTE[2], label="Ensemble")], loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=8, frameon=False)
    savefig("04_model_comparison.png")

    best_pred = p_ens if s["RMSE"] < reg_scores(y_te, gs_ridge.predict(T_te))["RMSE"] else gs_ridge.predict(T_te)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    ax[0].scatter(y_te, best_pred, s=8, alpha=0.45, color=PALETTE[0])
    lim = [min(y_te.min(), best_pred.min()) - .2, max(y_te.max(), best_pred.max()) + .2]
    ax[0].plot(lim, lim, c=PALETTE[3], lw=1)
    ax[0].set_xlabel("Actual BT_easiness"); ax[0].set_ylabel("Predicted")
    ax[0].set_title(f"Predicted vs actual (test, R² = {r2_score(y_te, best_pred):.2f})")
    resid = y_te - best_pred
    sns.histplot(resid, bins=40, kde=True, color=PALETTE[1], ax=ax[1])
    ax[1].set_title(f"Residuals (mean {resid.mean():.3f}, SD {resid.std():.3f})")
    ax[1].set_xlabel("Actual - predicted")
    savefig("05_pred_vs_actual.png")
    out["residuals"] = {"mean": float(resid.mean()), "sd": float(resid.std()),
                        "shapiro_p_sample500": float(stats.shapiro(resid[:500])[1])}
    # error by genre
    cat_te = df["Categ"].values[idx_te]
    out["error_by_genre"] = {c: rmse(y_te[cat_te == c], best_pred[cat_te == c]) for c in ("Lit", "Info")}

    # Permutation importance of GBR on hand features
    pi = permutation_importance(gs_gb.best_estimator_, F_te, y_te, n_repeats=10, random_state=SEED, n_jobs=-1)
    imp = pd.Series(pi.importances_mean, index=FEATURE_NAMES).sort_values()
    out["permutation_importance_gbr"] = {k: float(v) for k, v in imp.items()}
    plt.figure(figsize=(8, 6))
    plt.barh(imp.index, imp.values, xerr=pi.importances_std[np.argsort(pi.importances_mean)], color=PALETTE[0])
    plt.xlabel("Increase in MSE when the feature is shuffled")
    plt.title("Permutation importance (tuned Gradient Boosting)")
    savefig("06_permutation_importance.png")

    # Learning curve for the best text model
    sizes, tr_sc, va_sc = learning_curve(gs_ridge.best_estimator_, T_tr, y_tr, cv=kf,
                                         train_sizes=np.linspace(0.1, 1.0, 6),
                                         scoring="neg_root_mean_squared_error", n_jobs=-1)
    plt.figure(figsize=(7, 4.5))
    plt.plot(sizes, -tr_sc.mean(1), "o-", c=PALETTE[0], label="Training RMSE")
    plt.plot(sizes, -va_sc.mean(1), "o-", c=PALETTE[1], label="Validation RMSE")
    plt.fill_between(sizes, -va_sc.mean(1) - va_sc.std(1), -va_sc.mean(1) + va_sc.std(1), alpha=.2, color=PALETTE[1])
    plt.xlabel("Training passages"); plt.ylabel("RMSE"); plt.legend()
    plt.title("Learning curve - Features + TF-IDF + Ridge")
    savefig("07_learning_curve.png")
    out["learning_curve"] = {"sizes": sizes.tolist(), "train": (-tr_sc.mean(1)).tolist(), "val": (-va_sc.mean(1)).tolist()}

    # Ridge alpha curve
    g = tuned["Features + TF-IDF + Ridge"]["grid"]
    plt.figure(figsize=(6, 4))
    plt.plot([float(k) for k in g], list(g.values()), "o-", c=PALETTE[0])
    plt.xscale("log"); plt.xlabel("Ridge alpha (log scale)"); plt.ylabel("5-fold CV RMSE")
    plt.title("Effect of regularisation strength")
    savefig("08_ridge_alpha.png")

    # 9. Classification -------------------------------------------------------
    clf_models = {
        "Logistic Regression (features)": (Pipeline([("sc", StandardScaler()),
                                                     ("m", LogisticRegression(max_iter=2000, C=1.0))]), "F"),
        "Random Forest (features)": (RandomForestClassifier(400, min_samples_leaf=2, n_jobs=-1, random_state=SEED), "F"),
        "Multinomial Naive Bayes (TF-IDF)": (Pipeline([("tf", tfidf_word()), ("m", MultinomialNB(alpha=0.3))]), "T"),
        "Linear SVM (TF-IDF)": (Pipeline([("tf", tfidf_word()), ("m", LinearSVC(C=0.5))]), "T"),
        "Logistic Regression (features + TF-IDF)": (Pipeline([
            ("u", FeatureUnion([("tf", tfidf_word()),
                                ("hf", Pipeline([("h", HandFeatures()), ("sc", StandardScaler()),
                                                 ("w", FunctionTransformer(down_weight_sparse))]))])),
            ("m", LogisticRegression(max_iter=3000, C=4.0))]), "T"),
    }
    crow, best_clf = [], (None, -1, None)
    for name, (m, kind) in clf_models.items():
        Xtr, Xte = (F_tr, F_te) if kind == "F" else (T_tr, T_te)
        m.fit(Xtr, lab_tr)
        p = m.predict(Xte)
        acc, f1 = accuracy_score(lab_te, p), f1_score(lab_te, p, average="macro")
        crow.append({"Model": name, "Accuracy": acc, "Macro F1": f1})
        print(f"  {name:40s} acc {acc:.3f} F1 {f1:.3f}")
        if f1 > best_clf[1]:
            best_clf = (name, f1, p)
    cres = pd.DataFrame(crow)
    cres.to_csv(os.path.join(RES, "classification_results.csv"), index=False)
    out["classification"] = cres.round(4).to_dict(orient="records")
    order = ["Hard", "Medium", "Easy"]
    cm = confusion_matrix(lab_te, best_clf[2], labels=order)
    out["best_classifier"] = {"name": best_clf[0], "confusion_matrix": cm.tolist(),
                              "report": classification_report(lab_te, best_clf[2], labels=order, output_dict=True)}
    plt.figure(figsize=(5.5, 4.5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=order, yticklabels=order, cbar=False)
    plt.xlabel("Predicted"); plt.ylabel("Actual")
    plt.title(f"Confusion matrix\n{best_clf[0]}", fontsize=10)
    savefig("09_confusion_matrix.png")

    # 10. Unsupervised view: PCA + K-Means -----------------------------------
    Z = StandardScaler().fit_transform(F.values)
    pca = PCA(n_components=2, random_state=SEED).fit(Z)
    P = pca.transform(Z)
    km = KMeans(3, n_init=10, random_state=SEED).fit(Z)
    out["pca"] = {"explained_variance": pca.explained_variance_ratio_.tolist(),
                  "kmeans_ari_vs_difficulty": float(adjusted_rand_score(labels, km.labels_))}
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    for lab, c in zip(order, [PALETTE[3], PALETTE[1], PALETTE[2]]):
        mk = labels == lab
        ax[0].scatter(P[mk, 0], P[mk, 1], s=5, alpha=.4, color=c, label=lab)
    ax[0].legend(markerscale=3); ax[0].set_title("PCA of features, coloured by true difficulty")
    ax[0].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.0f}% var)")
    ax[0].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.0f}% var)")
    ax[1].scatter(P[:, 0], P[:, 1], s=5, alpha=.4, c=km.labels_, cmap="viridis")
    ax[1].set_title(f"K-Means clusters (k=3), ARI = {out['pca']['kmeans_ari_vs_difficulty']:.2f}")
    ax[1].set_xlabel("PC1"); ax[1].set_ylabel("PC2")
    savefig("10_pca_kmeans.png")

    # 11. Save models --------------------------------------------------------
    final_text = gs_ridge.best_estimator_
    final_text.fit(df["Excerpt"].values, y)  # refit on all data for deployment
    joblib.dump({"model": final_text, "tertile_cuts": [q1, q2]}, os.path.join(MOD, "best_regressor.joblib"),
                compress=3)

    # Light model for the JS backend: Ridge on hand features (no text vocab needed)
    ridge = Pipeline([("sc", StandardScaler()), ("m", Ridge(alpha=1.0))]).fit(F_tr, y_tr)
    light = reg_scores(y_te, ridge.predict(F_te))
    ridge.fit(F.values, y)
    sc, m = ridge.named_steps["sc"], ridge.named_steps["m"]
    export = {
        "model": "Ridge regression on 19 hand-crafted features (StandardScaler + Ridge, alpha=1.0)",
        "target": "BT_easiness (CLEAR corpus); higher = easier",
        "trained_on": len(df),
        "test_metrics_before_refit": light,
        "features": FEATURE_NAMES,
        "mean": sc.mean_.tolist(),
        "scale": sc.scale_.tolist(),
        "coef": m.coef_.tolist(),
        "intercept": float(m.intercept_),
        "tertile_cuts": [float(q1), float(q2)],
        "common_words": sorted(COMMON_WORDS),
    }
    with open(os.path.join(MOD, "ridge_features.json"), "w") as f:
        json.dump(export, f, indent=1)
    # same model as a <script> include for the zero-install index.html demo
    with open(os.path.join(ROOT, "shared", "ridge_model.js"), "w") as f:
        f.write("// Generated by ml/train.py - do not edit by hand
window.RIDGE_MODEL = ")
        json.dump(export, f)
        f.write(";
")
    out["deployed_light_model"] = light

    # sample feature vectors for JS parity test
    sample = df.sample(25, random_state=1)
    pd.DataFrame({"text": sample["Excerpt"].values,
                  "pred": ridge.predict(feature_frame(sample["Excerpt"].tolist()).values)}).to_json(
        os.path.join(RES, "parity_samples.json"), orient="records")

    out["runtime_sec"] = round(time.time() - t0, 1)
    with open(os.path.join(RES, "metrics.json"), "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"Done in {out['runtime_sec']} s")


if __name__ == "__main__":
    main()
