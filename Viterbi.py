from tqdm import tqdm
import sys

def generate_probability_count(filename):
    file = open(filename, "r")
    lines = file.readlines()

    word_tag_count={}
    tag_count={}
    tag_bigram_count={}
    prob_tag_bigram={}
    prob_word_tag={}
    tag_count['SoS']=0

    for line in tqdm(lines,desc="Generating probability count"):
        input_line = list(line.strip().split(' '))
        first_word = 0

        tag_count['SoS']+=1
        for i in range(len(input_line)):
            input_line[i]=input_line[i].lower()

            if(i < (len(input_line)-1)):
                input_line[i+1]=input_line[i+1].lower()

            split_char='/'
            split_counter = input_line[i].count(split_char)
            if(split_counter>1):
                temp = list(input_line[i].strip().split(split_char))
                each_word = split_char.join(temp[:2]), split_char.join(temp[2:])
                each_word = list(each_word)
            else:
                each_word = list(input_line[i].strip().split(split_char))

            next_word = list(input_line[i+1].strip().split('/')) if(i < (len(input_line)-1)) else " "

            #count of tags    
            if("|" in each_word[-1]):
                each_tag = list(each_word[-1].strip().split('|'))
                for i in range(len(each_tag)):
                    if(each_tag[i] not in tag_count): 
                        tag_count[each_tag[i]]=1
                    else:
                        tag_count[each_tag[i]]+=1
                    
                    #corpus of word,tag and their count and probabilities            
                    if((each_word[0],each_tag[i]) not in word_tag_count):
                        word_tag_count[(each_word[0],each_tag[i])]=1
                        if(each_tag[i] in tag_count):
                            prob_word_tag[(each_word[0],each_tag[i])]= round((word_tag_count[(each_word[0],each_tag[i])] / tag_count[each_tag[i]]),7)
                    else:
                        word_tag_count[(each_word[0],each_tag[i])]+=1
                        if(each_tag[i] in tag_count):
                            prob_word_tag[(each_word[0],each_tag[i])]= round((word_tag_count[(each_word[0],each_tag[i])] / tag_count[each_tag[i]]),7)

                    #corpus of bigrams of tags with "|" and their count and probabilities for start of sentence
                    if(first_word==0):
                        if(('SoS',each_tag[i]) not in tag_bigram_count):
                            tag_bigram_count[('SoS',each_tag[i])]=1
                            first_word+=1
                            prob_tag_bigram[(each_tag[i],'SoS')] = round((tag_bigram_count[('SoS',each_tag[i])] / tag_count[each_tag[i]]),7)              
                        else:
                            tag_bigram_count[('SoS',each_tag[i])]+=1
                            first_word+=1  
                            prob_tag_bigram[(each_tag[i],'SoS')] = round((tag_bigram_count[('SoS',each_tag[i])] / tag_count[each_tag[i]]),7)

                    #corpus of bigrams of tags and their count and probabilities for not start of sentence
                    if((each_tag[i],next_word[-1]) not in tag_bigram_count):
                        tag_bigram_count[(each_tag[i],next_word[-1])]=1
                        prob_tag_bigram[(next_word[-1],each_tag[i])] = round((tag_bigram_count[(each_tag[i],next_word[-1])] / tag_count[each_tag[i]]),7)
                    else:
                        tag_bigram_count[(each_tag[i],next_word[-1])]+=1  
                        prob_tag_bigram[(next_word[-1],each_tag[i])] = round((tag_bigram_count[(each_tag[i],next_word[-1])] / tag_count[each_tag[i]]),7)

            else:
                if(each_word[-1] not in tag_count):
                    tag_count[each_word[-1]]=1
                else:
                    tag_count[each_word[-1]]+=1
                
                #corpus of word,tag without "|" and their count and probabilities
                if((each_word[0],each_word[-1]) not in word_tag_count):
                    word_tag_count[(each_word[0],each_word[-1])]=1
                    prob_word_tag[(each_word[0],each_word[-1])]= round((word_tag_count[(each_word[0],each_word[-1])] / tag_count[each_word[-1]]),7)
                else:
                    word_tag_count[(each_word[0],each_word[-1])]+=1
                    prob_word_tag[(each_word[0],each_word[-1])]= round((word_tag_count[(each_word[0],each_word[-1])] / tag_count[each_word[-1]]),7)

                #corpus of bigrams of tags and their count and probabilities for start of sentence 
                if(first_word==0):
                    if(('SoS',each_word[-1]) not in tag_bigram_count):
                        tag_bigram_count[('SoS',each_word[-1])]=1
                        first_word+=1
                        prob_tag_bigram[(each_word[-1],'SoS')] = round((tag_bigram_count[('SoS',each_word[-1])] / tag_count[each_word[-1]]),7)              
                    else:
                        tag_bigram_count[('SoS',each_word[-1])]+=1
                        first_word+=1  
                        prob_tag_bigram[(each_word[-1],'SoS')] = round((tag_bigram_count[('SoS',each_word[-1])] / tag_count[each_word[-1]]),7)

                #corpus of bigrams of tags and their count and probabilities for not start of sentence
                if((each_word[-1],next_word[-1]) not in tag_bigram_count):
                    tag_bigram_count[(each_word[-1],next_word[-1])]=1
                    prob_tag_bigram[(next_word[-1],each_word[-1])] = round((tag_bigram_count[(each_word[-1],next_word[-1])] / tag_count[each_word[-1]]),7)
                else:
                    tag_bigram_count[(each_word[-1],next_word[-1])]+=1  
                    prob_tag_bigram[(next_word[-1],each_word[-1])] = round((tag_bigram_count[(each_word[-1],next_word[-1])] / tag_count[each_word[-1]]),7)
    
    tag_list = list(tag_count)
    
    for i in range(len(tag_list)):
        for j in range(len(tag_list)):
            if((tag_list[i],tag_list[j]) not in tag_bigram_count):
                tag_bigram_count[(tag_list[i],tag_list[j])]=0
            var1=(tag_bigram_count[(tag_list[i],tag_list[j])] +1)
            prob_tag_bigram[(tag_list[j],tag_list[i])] = round((var1/(tag_count[tag_list[i]] + len(tag_list))),7)
                                                                      
    file.close()        
    return list(tag_count), prob_word_tag, prob_tag_bigram
                                                               
def viterbi_algorithm(filename, tag_list, prob_word_tag, prob_tag_bigram):
    file = open(filename, "r")
    lines = file.readlines()
    
    score={}
    back_ptr={}
    list_of_sequences=[]
    list_of_test_sequences=[]

    out_file = open("POS.test.out", "a")
    total_ct = 0
    correct_predict_ct = 0
    val = 0
    for line in tqdm(lines,desc="testing..."):
        next_line = ""
        each_word_input=[]
        ground_truth_tag=[]
        input_line = list(line.strip().split(' '))
        for i in range(len(input_line)):
            input_line[i]=input_line[i].lower()
            input_ = list(input_line[i].strip().split('/'))
            each_word_input.append(input_[0])
            ground_truth_tag.append(input_[-1])

        #Initialization Step 
        for i in range(len(tag_list)):
            if(((each_word_input[0],tag_list[i]) in prob_word_tag ) and ((tag_list[i],'SoS') in prob_tag_bigram ) ):
                score[(each_word_input[0],tag_list[i])] = prob_word_tag[(each_word_input[0],tag_list[i])] * prob_tag_bigram[(tag_list[i],'SoS')]
            else:
                score[(each_word_input[0],tag_list[i])] = 0
            back_ptr[(each_word_input[0],tag_list[i])] = 0

        #Iteration Step
        count=list(range(len(each_word_input)))
        for i in count[1:]:
            new_word=0
            for j in range(len(tag_list)):
                max_value,value=0,0
                tag='nn'
                for k in range(len(tag_list)):
                    if(((each_word_input[i-1],tag_list[k]) in score) and ((tag_list[j],tag_list[k]) in prob_tag_bigram)):
                        value = score[(each_word_input[i-1],tag_list[k])] * prob_tag_bigram[(tag_list[j],tag_list[k])]
                    #Find max
                        if(max_value <= value):
                            max_value = value
                            tag = tag_list[k]

                if((each_word_input[i],tag_list[j]) in prob_word_tag):
                    new_word+=1
                    score[(each_word_input[i],tag_list[j])] = prob_word_tag[(each_word_input[i],tag_list[j])] * max_value 
                back_ptr[(each_word_input[i],tag_list[j])] = tag
            if(new_word==0):
                prob_word_tag[(each_word_input[i],'nn')] = 1
                score[(each_word_input[i],'nn')] = prob_word_tag[(each_word_input[i],'nn')] * max_value

        max_score=0
        last_tag='nn'
        for i in range(len(tag_list)):
            if((each_word_input[len(each_word_input)-1],tag_list[i]) in score ):
                if((max_score < score[each_word_input[len(each_word_input)-1],tag_list[i]])):
                    max_score = score[(each_word_input[len(each_word_input)-1],tag_list[i])]
                    tag = back_ptr[(each_word_input[len(each_word_input)-1],tag_list[i])]
                    last_tag = tag_list[i]
        next_line = each_word_input[len(each_word_input)-1] + "/" + last_tag
        total_ct += 1
        if(last_tag ==ground_truth_tag[-1]):
            correct_predict_ct += 1
        tag_of_nextword = tag

        for i in reversed(range(len(each_word_input)-1)):
            total_ct += 1
            next_line = each_word_input[i] + "/" + tag_of_nextword +" "+ next_line
            if(tag_of_nextword==ground_truth_tag[i]):
                correct_predict_ct += 1
            tag_of_nextword = back_ptr[each_word_input[i],tag_of_nextword]
        next_line = next_line + "\n"
        out_file.write(next_line)
        val += 1

    out_file.close()
    file.close()
    return ((correct_predict_ct/total_ct)*100)
                                                               
if __name__ == "__main__":
    arguments = sys.argv  
    train_file = str(arguments[1])
    test_file = str(arguments[2])
    
    #get count of probabilities 
    tag_list, prob_word_tag, prob_tag_bigram = generate_probability_count(train_file)
    
    #giving POS tags
    accuracy = viterbi_algorithm(test_file, tag_list, prob_word_tag, prob_tag_bigram)
    
    print("Accuracy = ")
    print(accuracy)