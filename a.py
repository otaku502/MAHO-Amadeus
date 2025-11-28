import requests

url = "http://127.0.0.1:9880"
data = {
    "refer_wav_path": r"C:\Users\19045\Desktop\MAHO\backend\data\TTS-audio\激动.wav",
    "prompt_text": "あら、あなた。",
    "prompt_language": "ja",
    "text": "久しぶり",
    "text_language": "ja",
    "speed": 1.2,           # 语速
    "top_k": 20,            # 可选
    "top_p": 0.7,           # 可选
    "temperature": 0.7,     # 可选
    "sample_steps": 40      # 可选
}

response = requests.post(url, json=data)
print("状态码:", response.status_code)
if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("音频已保存为 output.wav")
else:
    print("返回内容:", response.text)