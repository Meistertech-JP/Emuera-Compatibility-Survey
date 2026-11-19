# 省略観測の限定追補

この追補は、同じcase IDの既存観測記録に、対応するsource記録の構造化観測から選別した値を加えます。38件を収録し、case ID、typed target、verdict、既存limitationsを併記します。値は保存済みsource記録の投影で、新しい実行や独立再現ではありません。

TRYTRANSFER285の4 caseは、各caseのnative-01、native-02、public-01を分けて整数markerを掲載します。合計90値です。keyは識別子形です。mode間で値が等しくても統合しません。

他caseは選択したkeyの観測値だけを収録します。diagnostic、postfatal_values、value_body_execution、after_present、done_present等のfield名だけから実測とは判断せず、source値と親mode/sideに基づき、値、null、UNOBSERVED、false、未到達を区別します。元raw path/hash、process情報、長いdiagnostic raw行は同梱しません。未選択・未知fieldは未評価であり、観測なしの証拠ではありません。

省略された49 diagnostic位置の内訳は空値40・OUTPUTLOG警告9です。空値は空値として残し、警告は保存先を除いて示します。54個のpostfatal_valuesは48個がUNOBSERVED、6個がnot_a_fatal_observation。36個のvalue_body_executionは30個がUNOBSERVED、6個がnot_calledです。after_present/done_presentは各18個のbool値で、true 6・false 12。これらはcase数ではなく重複を含むfield位置数です。

各行はsource record pointer、record byte SHA-256、field SHA-256を記録します。verdictとtyped targetは対応するcase台帳・source記録と照合されます。古い486-record snapshotの後に記録された2件の停止後state修正は `current-candidate-corrections.jsonl` に別収録し、修正後の値・limitations・pointer・line/record hashを示します。古いprojectionを最新記録として扱いません。既存の値とlimitationsは `base_recovery` に保持し、この2件は修正後記録を先に確認してください。

## 検証と資料範囲

486件の公開観測JSONLは親bundle rootの `observations.jsonl` に含まれ、この子ディレクトリには重複同梱していません。source照合用の元486件snapshot（verifier内SHA-256 `e11cc635d258949af41d74b30e1157dab02d95b35c9825200066c3ed07a4a515`）、source register、現行case register、元raw files、source receipts、独立verifier/manifest pinは配布されず、取得経路も案内しません。source verifierには、公開projectionとは別に、この固定snapshotとsource register・case registerが必要です。独立pinが別途提供された場合は、実行前に `verify.py` のSHA-256をそのpinと照合し、対応する独立manifest SHA-256をverifierに渡してください。独立pinがない場合にできるのは同梱manifestとbundle構造の自己整合性確認で、発行元やsourceの真正性確認ではありません。

verifierはfile hashes、38 case identities、mode marker values、引き継いだlimitations、source field hashes、typed targets/verdictsを照合します。raw全体の真正性や実測の意味を独立に証明するものではなく、未同梱receiptの存在も確認しません。配布条件や権利の判断もこの追補の範囲外です。

親bundle root（`query.py`、`verify_bundle.py`、`manifest.json` があるディレクトリ）から次を実行します。

```powershell
python -B verify_bundle.py
python -B file_set_manifest.py verify --manifest manifest.json --root public=.
python -B query.py --case CASE_ID
```
[親bundleのcase/typed target検索](../query.py)
