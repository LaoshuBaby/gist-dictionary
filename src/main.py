import requests
import fastapi
import uvicorn

def init():
    # 交互式填写必要信息和创建config
    pass

def get_config():
    pass

def get_gist_content():
    # 需要获取的gist名字需要提前放在配置文件里面，建议写一个init过程
    # 这块的读取文档在 https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#get-a-gist

    pass

def put_gist_content():
    pass

def authentication():

    # 获取gist访问的时候需要一个github的token，这个可以从系统环境变量去获得，并且不推荐明文存储在任何文件中因为这个太危险了。
    # 其实系统环境变量也是非常危险的
    # 还是优先看有没有github官方指定的环境变量名，有，https://cli.github.com/manual/gh_help_environment
    import os
    print(os.environ.get("GH_TOKEN",None))
    pass

def main():
    authentication()
    pass

if __name__ == "__main__":
    main()