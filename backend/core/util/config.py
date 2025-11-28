import yaml

def load_yaml(file_path):
		"""
		从指定的YAML文件加载配置。

		参数:
				file_path (str): YAML文件的路径。

		返回:
				dict: 加载的配置字典。
		"""
		with open(file_path, 'r', encoding='utf-8') as file:
				config = yaml.safe_load(file)
		return config
