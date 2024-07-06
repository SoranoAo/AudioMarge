import json
from pydub import AudioSegment
import os
from datetime import datetime

def read_file_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def read_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def concatenate_audio_files(config):
    input_dir = config["input_directory"]
    output_dir = config["output_directory"]
    silence_between_files = config["silence_between_files"]
    silence_at_start = config["silence_at_start"]
    silence_at_end = config["silence_at_end"]
    file_list_path =config["file_list"]

    # 無音区間を作成
    silence_between = AudioSegment.silent(duration=silence_between_files)
    silence_start = AudioSegment.silent(duration=silence_at_start)
    silence_end = AudioSegment.silent(duration=silence_at_end)

    # テキストファイルから音声ファイルのリストを読み込む
    file_list = read_file_list(file_list_path)
    file_list = [os.path.join(input_dir, file) for file in file_list]

    # 初期の空のオーディオセグメントに開始の無音区間を追加
    combined = silence_start

    # 各ファイルを読み込んで結合
    for file_name in file_list:
        audio = AudioSegment.from_file(file_name)
        combined += audio + silence_between

    # 最後の無音区間を削除して、終了の無音区間を追加
    combined = combined[:-len(silence_between)] + silence_end

    # 現在の日付と時刻を取得してファイル名に追加
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"merged_file_{current_time}.wav")

    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)

    # 結合したオーディオをファイルに書き出し
    combined.export(output_file, format="wav")

if __name__ == "__main__":
    config_path = "config.json"
    
    # 設定ファイルから設定を読み込む
    config = read_config(config_path)
    
    # 音声ファイルを結合
    concatenate_audio_files(config)
