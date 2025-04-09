def authentication(token:str=""):

    # 获取gist访问的时候需要一个github的token，这个可以从系统环境变量去获得，并且不推荐明文存储在任何文件中因为这个太危险了。
    # 其实系统环境变量也是非常危险的
    # 还是优先看有没有github官方指定的环境变量名，有，https://cli.github.com/manual/gh_help_environment
    try:
        GH_TOKEN=os.environ.get("GH_TOKEN",None)
        GITHUB_TOKEN =os.environ.get("GITHUB_TOKEN",None)
        if GH_TOKEN!=None and GH_TOKEN!="":
            TOKEN=GH_TOKEN
        elif GITHUB_TOKEN!=None and GITHUB_TOKEN!="":
            TOKEN=GITHUB_TOKEN
        else:
            TOKEN=token
    except Exception as e:
        print(e)
        TOKEN=token

    print(TOKEN)
    pass