
import os


classpath={}

def listresult():
    count=0
    #path='/Users/jarek-mac/THU/ipolicy/Htmlunit/result'
    #path = '/Users/jarek-mac/THU/ipolicy/文本分析/result_lar'
    path='/Users/jarek-mac/THU/ipolicy/文本分析/20180130标题爬虫/地方'
    #path = '/Users/jarek-mac/THU/ipolicy/文本分析/20180130标题爬虫/中央'
    resultpath=[]
    files = os.listdir(path)
    for file in files:
        resultpath.append(path+'/'+file)
    for path in resultpath:
        number=path[-7:-4]
        try:
            classname=classpath[number]
        except Exception as e:
            classname='notype'
        titles = readfile(path)
        if titles!=None:
            for title in titles:
                with open("/Users/jarek-mac/THU/ipolicy/文本分析/20180130标题爬虫/tags.txt", "a+") as f:
                    f.write(classname + '$ipolicy$' + title + '\n')
                    count+=1
    print(count)

def readclass():
    #path='/Users/jarek-mac/THU/ipolicy/Htmlunit/大类对应.txt'
    path='/Users/jarek-mac/THU/ipolicy/文本分析/20180130标题爬虫/大类对应.txt'
    f=open(path,'r')
    lines=[]
    line = f.readline()  # 调用文件的 readline()方法
    lines.append(line)


    while line:
        line = f.readline()
        lines.append(line)
    for line in lines:
        line=line.replace('\n','')
        line=line.replace('\ufeff','')
        try:
            index=line.index(':')
            number=line[:index]
            name=line[index+1:]
            classpath[number]=name
        except Exception as e:
            print('解析类标出现错误')


    print(classpath)


def readfile(path):
    titles = []
    lines = []
    try:
        f = open(path,'r',encoding='gb2312')  # 返回一个文件对象

        line = f.readline()  # 调用文件的 readline()方法
        lines.append(line)
        print('gb2312')

    except :
        try:
            f = open(path, 'r', encoding='utf-8')  # 返回一个文件对象

            line = f.readline()  # 调用文件的 readline()方法
            lines.append(line)
            print('utf-8')
        except:
            try:
                f = open(path, 'r', encoding='GBK')  # 返回一个文件对象

                line = f.readline()  # 调用文件的 readline()方法
                lines.append(line)
                print('GBK')
            except:
                print(path)
                return


    while line:
        # print(line), # 后面跟 ',' 将忽略换行符
        # print(line, end = '')　　　# 在 Python 3中使用
        try:
            line = f.readline()
            lines.append(line)
        except Exception as e:
            continue
        #print(path)
        #




    for i in range(len(lines)):
        if '展开' in lines[i]:
            title = lines[i - 1]
            try:
                title.replace('\n', '')
                index = title.index('\t')
                title = title[index + 1:]
                titles.append(title)
            except Exception as e:
                continue
    f.close()
    return titles


if __name__ == '__main__':
    print('reading class')
    readclass()
    print('reading text')
    listresult()

