from tqdm import tqdm
import sys

if __name__ == "__main__":
    arguments = sys.argv  
    test_file = str(arguments[2])
    train_file = open(str(arguments[1]),"r")

    lines = train_file.readlines()

    word_corpus=[]
    word_tag_corpus={}
    tag_corpus=[]

    count=0
    for line in tqdm(lines, desc = "Generate word tag count"):
        count+=1
        input_line = list(line.strip().split(' '))
        first_word=0

        for i in range(len(input_line)):

            input_line[i]=input_line[i].lower()

            split_char='/'
            split_counter = input_line[i].count(split_char)
            #each word will be of size 2 always now..
            if(split_counter>1):
                temp = list(input_line[i].strip().split(split_char))
                each_word = split_char.join(temp[:2]), split_char.join(temp[2:])
                each_word = list(each_word)
            else:
                each_word = list(input_line[i].strip().split(split_char))

            #corpus of words

            if(each_word[0] not in word_corpus):
                word_corpus.append(each_word[0])

            if("|" in each_word[-1]):
                each_tag = list(each_word[-1].strip().split('|'))
                for i in range(len(each_tag)):
                    if((each_word[0],each_tag[i]) not in word_tag_corpus): 
                        word_tag_corpus[each_word[0],each_tag[i]]=1
                    else:
                        word_tag_corpus[each_word[0],each_tag[i]]+=1

                    if(each_tag[i] not in tag_corpus):
                        tag_corpus.append(each_tag[i])
            elif((each_word[0],each_word[-1]) not in word_tag_corpus):
                word_tag_corpus[each_word[0],each_word[-1]]=1
                if(each_word[-1] not in tag_corpus):
                    tag_corpus.append(each_word[-1])
            else:
                word_tag_corpus[each_word[0],each_word[-1]]+=1
                if(each_word[-1] not in tag_corpus):
                    tag_corpus.append(each_word[-1])
    train_file.close()
    
    #baseline algorithm
    test_file = open(str(arguments[2]),"r")
    lines = test_file.readlines()
    total_ct = 0
    correct_predict_ct = 0


    for line in tqdm(lines, desc = "Test"):
        input_line = list(line.strip().split(' '))
        next_line = ""

        for i in range(len(input_line)):
            input_line[i]=input_line[i].lower()
            input_ = list(input_line[i].strip().split('/'))
            word_input= input_[0]
            max_value=0
            for j in range(len(tag_corpus)):
                if((word_input,tag_corpus[j]) in word_tag_corpus):
                    if(max_value < word_tag_corpus[(word_input,tag_corpus[j])]):
                        max_value = word_tag_corpus[(word_input,tag_corpus[j])]
                        tag = tag_corpus[j]
            if(max_value==0):
                tag="nn"
            total_ct += 1
            if(tag ==input_[-1]):
                correct_predict_ct += 1
    print("Accuracy:")
    print((correct_predict_ct/total_ct)*100)
    test_file.close()