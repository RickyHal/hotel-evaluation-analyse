from collections import Counter
import numpy as np

trainingDataFilePath = 'training-100000.txt'
modelFilePath = 'model-10000000.model'
testDataFilePath = 'test_1000.txt'
resultFilePath = '2016081111_侯海洋.result'
'''
function:cut the string
parameter:
    1.string:the input string
return:
    1.type:list,mean:a list include the cutted string
'''


def extractFeatures(string):
    return string.split(' ')


'''
function:save the model
parameter:
    1.goodModel:the good model dict,form is word-count like key-value
    2.badModel:the bad model dict,form is word-count like key-value
    3.goodCount:the good words' number,include the repeat words
    4.badCount:the bad words' number,include the repeat words
    5.V:the number of words,no repeat
return:
    1.type:bool,mean:save model success or fail
'''


def saveModel(goodModel, badModel, goodCount, badCount, V):
    try:
        global modelFilePath
        with open(modelFilePath, 'w', encoding='UTF-8-sig') as f:
            for key, value in goodModel.items():
                line = '好评_%s\t%s\r\n' % (key, value)
                f.write(line)
            for key, value in badModel.items():
                line = '差评_%s\t%s\r\n' % (key, value)
                f.write(line)
            line = '好评\t%s\r\n差评\t%s\r\nV\t%s' % (goodCount, badCount, V)
            f.write(line)
            f.close()
        return True
    except:
        return False


'''
function:load the model
parameter:None
return:list,mean:the model,include good words model,bad words model,goodCount,badCount and V
'''


def loadModel():
    try:
        model, goodModel, badModel, count = {}, {}, {}, {}
        words = set()
        global modelFilePath
        with open(modelFilePath, "r", encoding='UTF-8-sig') as f:
            for line in f:
                line = line.replace('\r\n', '')
                if line[0:3] == '好评_':
                    goodModel[line.split('\t')[0].split(
                        '_')[1]] = float(line.split('\t')[1])
                    words.add(line.split('\t')[0].split('_')[1])
                elif line[0:3] == '差评_':
                    badModel[line.split('\t')[0].split(
                        '_')[1]] = float(line.split('\t')[1])
                    words.add(line.split('\t')[0].split('_')[1])
                elif line[0:2] == '好评':
                    count['goodCount'] = float(line.split('\t')[1])
                elif line[0:2] == '差评':
                    count['badCount'] = float(line.split('\t')[1])
        count['V'] = len(words)
        print(count['goodCount'] + count['badCount'])
        model['goodModel'] = goodModel
        model['badModel'] = badModel
        model['count'] = count
        print('load model success')
        f.close()
        return model
    except:
        print('load model fail')


'''
function:read all the lines of test data
parameter:None
return:list,mean:the test data list,it's item is a string
'''


def readAllLines():
    test = []
    global testDataFilePath
    with open(testDataFilePath, 'r', encoding='UTF-8-sig') as f:
        line = f.readline().replace('\n', '')
        while line:
            test.append(line)
            line = f.readline().replace('\n', '')
    return test

'''
function:save the predict result
parameter:
    1.result:the predict result
return:bool
'''


def saveResult(result):
    global resultFilePath
    try:
        with open(resultFilePath, 'w') as f:
            for item in result:
                f.write(item + '\n')
        return True
    except:
        return False

'''
function:train the model
parameter:None
return:None
'''


def train():
    # mapper
    goodWords, badWords = [], []
    global trainingDataFilePath
    with open(trainingDataFilePath, 'r', encoding='UTF-8-sig') as f:
        for line in f:
            line = line.replace('\n', '')
            if line[0:2] == '好评':
                goodWords.extend(line[2:].strip('\t').split(' '))
            else:
                badWords.extend(line[2:].strip('\t').split(' '))
    # reducer
    goodModel = dict(Counter(goodWords))
    badModel = dict(Counter(badWords))
    V = len(set(goodWords + badWords))
    print(V)
    goodCount, badCount = len(goodWords), len(badWords)
    # save model
    if saveModel(goodModel, badModel, goodCount, badCount, V):
        print('store model success')
    else:
        print('store model fail')


'''
function:predict one
parameter:
    1.comment:one comment
    2.model:the model
return:string,mean:'好评' or '差评'
'''


def predict(comment, model):
    if model:
        comment = extractFeatures(comment)
        V = model['count']['V']
        print(V)
        # print(V, model['count']['goodCount'], model['count']['badCount'])
        p_good_before = np.log(model['count'][
                               'goodCount'] / (model['count']['goodCount'] + model['count']['badCount']))
        p_bad_before = np.log(model['count'][
                              'badCount'] / (model['count']['goodCount'] + model['count']['badCount']))
        p_good_word, p_bad_word = 0, 0
        for word in comment:
            if word in model['goodModel'].keys():
                p_good_word += np.log((model['goodModel'][word] + 1.0) /
                                      (model['count']['goodCount'] + V))
            else:
                p_good_word += np.log(1.0 / (model['count']['goodCount'] + V))
            if word in model['badModel'].keys():
                p_bad_word += np.log((model['badModel'][word] + 1.0) /
                                     (model['count']['badCount'] + V))
            else:
                p_bad_word += np.log(1.0 / (model['count']['badCount'] + V))
        p_good_after = p_good_before + p_good_word
        p_bad_after = p_bad_before + p_bad_word
        if p_good_after > p_bad_after:
            return '好评'
        else:
            return '差评'

'''
function:predict all
parameter:model
return:None
'''


def predictAll(model):
    result = []
    accuracy, amount = 0, 0
    test = readAllLines()
    for line in test:
        gold = line[0:2]
        prediction = predict(line[2:].strip('\t').strip('\n'), model)
        # print((amount + 1),
        #       'Gold={0}\tPrediction={1}'.format(gold, prediction))
        if gold == prediction:
            accuracy += 1
        print(amount + 1,
              'Gold={0}\tPrediction={1}'.format(gold, prediction))
        amount += 1
        result.append(prediction)
    print("Accuracy = {0}%".format(str(round((accuracy / amount) * 100, 5))))
    print('正确=', accuracy, '错误=', amount)
    result.append("Accuracy = {0}%".format(
        str(round((accuracy / amount) * 100, 5))))
    if saveResult(result):
        print("save result success")
    else:
        print("save result fail")


'''
function:main function
parameter:None
return:None
'''


def main():
    # train()
    model = loadModel()
    if model:
            # print(model['count']['V'])
            # print(model)
            # comment = '几乎 凌晨 才 到 包头 包头 没有 什么 特别 好 酒店 每次 来 就是 住 这家 所以 没有 忒 多 对比 感觉 行 下次 还是 得到 这里 来 住'
            # print(predict(comment, model))
        predictAll(model)
    else:
        print('load model fail')


if __name__ == '__main__':
    main()
