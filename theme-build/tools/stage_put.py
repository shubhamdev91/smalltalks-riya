"""stage_put.py <xgoogdate> <local> <uuid/filename> <signature> [mime]  -> PUT + verify md5 via public GET"""
import sys, subprocess, hashlib
date, local, path, sig = sys.argv[1:5]; mime = sys.argv[5] if len(sys.argv) > 5 else 'text/plain'
B = "https://shopify-staged-uploads.storage.googleapis.com/tmp/83023397077/files/"
Q = ("?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=merchant-assets%40shopify-tiers.iam.gserviceaccount.com"
     "%2F20261009%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=" + date + "&X-Goog-Expires=604800&X-Goog-SignedHeaders=host&X-Goog-Signature=" + sig)
put = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT", "-H", "Content-Type: " + mime, "--data-binary", "@" + local, B + path + Q], capture_output=True, text=True).stdout
body = subprocess.run(["curl", "-s", B + path], capture_output=True).stdout
ok = hashlib.md5(body).hexdigest() == hashlib.md5(open(local, 'rb').read()).hexdigest()
print(put, 'md5-ok' if ok else 'MD5-MISMATCH', B + path)
