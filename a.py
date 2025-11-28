import requests

url = "http://127.0.0.1:9880"
data = {
    "refer_wav_path": "C:/Users/19045/Desktop/MAHO/Model/TTS-Maho/WAV-MAHO/vocal_01_02_MAH0049.wav.reformatted.wav_10.wav_0000000000_0000096960.wav",
    "prompt_text": "一二三。",
    "prompt_language": "zh",
    "text": "测试一下接口是否能用。",
    "text_language": "zh"
}

response = requests.post(url, json=data)
print("状态码:", response.status_code)
if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("音频已保存为 output.wav")
else:
    print("返回内容:", response.text)