import hashlib,json,re,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
tag=re.sub(r"[^A-Za-z0-9_-]","_",sys.argv[1])[-32:]
out=root/("native-printk-crop-"+tag+".png")
r=subprocess.run([sys.executable,str(root/"capture_crop_only.py"),sys.argv[1],sys.argv[2],sys.argv[3],str(out)],capture_output=True,text=True)
record={"crop_returncode":r.returncode,"crop_path":str(out) if out.is_file() else None,"crop_sha256":hashlib.sha256(out.read_bytes()).hexdigest() if out.is_file() else None,"crop_size_bytes":out.stat().st_size if out.is_file() else None}
if out.is_file():
 from PIL import Image
 with Image.open(out) as im: record["crop_dimensions"]=list(im.size)
print(json.dumps(record,separators=(",",":")))
raise SystemExit(r.returncode)
