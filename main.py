import  mysql.connector as c
import random, time
from questions import *
# ================================ Gloabl variable for MySQL connectivity ==============================
pswd = input('enter password of your MySQL server:')
db = input('enter the name of database you would like to use for mysql connectivity:')
try:
       database = c.connect(database = db, host = 'localhost', user = 'root', passwd = pswd)
       cursor = database.cursor()
except:
       print('an error has occured!!, check if the name of the databse and paasword is correct or not!!')
# ================================ setting up the tables for MySQL ====================================
def setup_table():
       try:
              cursor.execute('drop table question;')
              cursor.execute('drop table quiz_stats;')
              databse.commit()
       except:
              cursor.execute('create table question(ID varchar(3), question varchar(300), is_multiple char(2), answer varchar(60));')
              cursor.execute('create table quiz_stats(s_no int, participant varchar(20), question_attempted int, wrong_answers int, correct_answers int, accuracy int, other varchar(20));')
              database.commit()
       try:
              cursor.execute('create table question(ID varchar(3), question varchar(300), is_multiple char(2), answer varchar(60));')
              cursor.execute('create table quiz_stats(s_no int, participant varchar(20), question_attempted int, wrong_answers int, correct_answers int, accuracy int, other varchar(20));')
              database.commit()
       except:
              pass

setup_table()

#================================ insert all questin and their answers in a seperate table ========================
def insert_data():
       answer = 0
       multiple = 0
       for question in QUESTION:
              if is_multiple(question):
                     answer = QUESTION[question][QUESTION[question]['correct_option'].upper()]
                     multiple = 'T'
              elif not is_multiple(question):
                     answer = QUESTION[question]['correct_answer']
                     multiple = 'F'
              ID = QUESTION[question]['ID']
              ques_data_tuple = (ID,question, multiple, answer)
              cursor.execute('insert into question values'+str(ques_data_tuple)+';')
              database.commit()

# ================= make a cheat file for participants so that participants can cheat a bit for quiz ====================
def insert_data_txt():
       data_list = []
       ques_no = 0
       for question in QUESTION:
              if is_multiple(question):
                     #print(QUESTION[question]['ID'])
                     answer = QUESTION[question][QUESTION[question]['correct_option'].upper()]
              elif not is_multiple(question):
                     answer = QUESTION[question]['correct_answer']
              ques_no += 1
              data_list.append('Q'+str(ques_no)+')' +question+':'+answer+'\n\n')
       with open('cheat.txt','w') as f:
              f.writelines(data_list)             

# ==================================== RULES OF THE QUIZ ===============================================
time.sleep(3)
print('\n\n')
print('                    welcome to !! GENERAL KNOWLEDGE QUIZ !! ')
print('-> plz read the rules carefully','\n')
time.sleep(5)
print('-> format of answering question is the correct option written in lower case for multiple choice question','\n')
time.sleep(5)
print('-> for fill ups you have to write the whole answer in lower case','\n')
time.sleep(5)
print('-> all the answer should be in porper format, good luck','\n')
time.sleep(5)
print('-> be seroius, the computer will be asking if your are ready or not for the quiz','\n'+'he will now allow you to partcipate if you did not respond','\n')
time.sleep(5)
print('-> each participant will answer a total of 30 question of different catagory','\n')
time.sleep(5)
print('-> if you give answer 8 times you will be disqualifeid','\n'+'disqulifeid participant or participant who has completed the quiz cannot be registered again','\n')
time.sleep(8)
print('-> you can skip any queston by pressing the enter key','\n')
time.sleep(5)
print('-> only 5 participants are allowed, one at a time, Good luck !!','\n\n')
time.sleep(3)
# ======================================= Participants dictionary ============================================
participants = {}

# =============================== All required function for quiz loop are declared here =========================
# performance of the pariticipant
def make_remarks(accuracy):
       if accuracy < 20:
              return 'poor'
       elif accuracy >= 20  and accuracy < 40:
              return 'not bad'
       elif accuracy >= 40 and accuracy < 60:
              return 'average'
       elif accuracy >= 60 and accuracy < 80:
              return 'good'
       elif accuracy >= 80 and accuracy < 100:
              return 'excellent'
       elif accuracy == 100:
              return ' !! GENEUIS !! '
              

#check whether a question is multiple choice or one word type question
def is_multiple(question):
       if len(QUESTION[question]) - 2 > 0:
              return True
       else:
              return False

# ======================== prepare question for the participants in a random order =============================
def make_question_list(num):
       done = 0
       ques_list = []
       while done < num:
              ques = random.choice([i for i in QUESTION.keys()])
              if not ques in ques_list:
                     ques_list.append(ques)
                     done += 1
       return ques_list

# ============================== MAIN QUIZ STARTING FUNCTION ==========================================
def start_quiz(name,s_no, participants_data):
       print('\n')
       #initialize all variables
       display_multiple = False
       display_single = False
       wrong_answer = 0
       asking = False
       correct_answer = 0
       max_wrong_answer = 8
       question_attempted = 0
       total_question = 30
       ques_no = 1
       other = 0
       question_list = make_question_list(total_question)
       for question in question_list:
              print('Q'+str(ques_no)+')', question)
              if is_multiple(question):      #if question is multiple choice
                     print('A.',QUESTION[question]['A'])
                     print('B.',QUESTION[question]['B'])
                     print('C.',QUESTION[question]['C'])
                     print('D.',QUESTION[question]['D'])
                     if not display_multiple:
                            ask = input('-> enter correct option (only lower case allowed):')
                            display_multiple =True
                     else:
                            ask = input('-> enter correct option:')
                     
              if not is_multiple(question):      #if question is one word
                     if not display_single:
                            ask = input('-> enter correct answer (only lower case allowed, every letter in lower case):')
                            display_single = True
                     else: 
                            ask = input('-> enter correct answer:')

              if len(ask) > 0:
                     question_attempted += 1
                     if is_correct_answer(question,ask):
                            print('>>> well done')
                            correct_answer += 1
                     if not is_correct_answer(question,ask):
                            print('>>> wrong answer')
                            wrong_answer += 1
                            if wrong_answer == max_wrong_answer:
                                   print('>>> you are disqualified, you answer too many wrong answer','\n'+'>>> next plz..')
                                   print('==============================================','\n\n')
                                   participants_data['is_disqualified'] = True
                                   break
              elif len(ask) == 0:
                     print('>>> skipped')
              print('==============================================')
              ques_no += 1
              print('\n')
       if not participants[name]['is_disqualified']:
              print('>>>',name,'you have answered all questions')
       if s_no < 5:
              print('>>> next plz..','\n\n')
       #insertion of performance
       if question_attempted == 0:
              accuracy = 0
       elif question_attempted > 0:       
              accuracy = (correct_answer/question_attempted) * 100
       if participants_data['is_disqualified']:
              other = 'DISQUALIFIED'
       else:
              other = make_remarks(accuracy)
       data_tuple = (s_no, name, question_attempted, wrong_answer, correct_answer, accuracy, other)
       cursor.execute('insert into quiz_stats values'+str(data_tuple)+';')
       database.commit()

# ================================= Useful function for MAIN LOOP for registeration ====================================               
# function that ask whether the player is ready or not 
def is_ready(r):
       if r in ['y','Y','yes']:
              return True
       if r in ['n','N','no']:
              return False
       else:
              return 'no response'

# function that checks if the answer to a question is correct or not
def is_correct_answer(question, answer):
       if is_multiple(question):
              if answer == QUESTION[question]['correct_option']:
                     return True
              else:
                     return False
       if not is_multiple(question):
              if answer == QUESTION[question]['correct_answer']:
                     return True
              else:
                     return False

# ask name of the participant 
def ask_name(tolerance):
       repeated = 0
       name_given = False
       name = input('enter your name:')
       if len(name) > 0:
              name_given = True
       elif len(name) == 0:
              print(">>> computer can't accept empty name of any participant")
              while repeated < tolerance:
                     name = input('-> plz enter your name:')
                     if len(name) > 0:
                            name_given = True
                            break
                     repeated += 1
       if not name_given:
              name = generate_name()
              print('>>> computer gave you a random name,',name,'this will be used as your default name')
       return name

# generate random name for the participant (if participant does not enter his/her name)
def generate_name():
       len_new_name = random.randint(4,10)
       chracter_list = [chr(i) for i in range(65,91)]
       chracter_list.extend(chr(j) for j in range(97,123))
       chracter_list.extend(str(k) for k in range(10))
       new_name = ''
       for i in range(len_new_name):
              character = random.choice(chracter_list)
              new_name += character
       return new_name

# ================================== MAIN LOOP FOR REGISTERATION =====================================              
def main():
       ask_ready_tol = 3
       ask_name_tol = 3
       max_participant = 5
       participated = 0
       can_continue = 0
       wrong_answer = 0
       correct_answer = 0
       max_wrong_answer = 8

# ================ ask the name of the participant of the participant for registeration =======================================
       while participated  < 5:
              name = ask_name(ask_name_tol)
              if name not in participants:
                     print('>>> hello',name+'!','\n')
                     can_continue = True
                     participants[name] = {'status':'new','is_disqualified':False, 'answered_r':False}
              if name in participants:
                     if not participants[name]['is_disqualified']:
                            if participants[name]['status'] == 'done':
                                   print('>>> same participant not allowed after completing the quiz')
                                   print('==============================================','\n')
                                   can_continue = False
                            if participants[name]['status'] == 'attempted':
                                   print('>>> you again hope you have preapred well this time','\n')
                                   participants[name]['answered_r'] = False
                                   can_continue = True
                     if participants[name]['is_disqualified']:
                            print('>>> you are already disqualified, it does not make sense for you too come back here')
                            print('==============================================','\n')
                            can_continue = False

# ================== ask the participant if he is ready to answer to take part in quiz or not ========================          
              if can_continue:
                     ready = input("-> are you ready for the quiz (reply in 'Y' or 'N'):")
                     if len(ready) > 0 and not is_ready(ready) == 'no response':
                            if is_ready(ready):
                                   print('>>> good')
                                   participants[name]['status'] = 'in_quiz'
                                   start_quiz(name, participated+1, participants[name])
                                   time.sleep(2.5)
                                   participated += 1
                                   participants[name]['status'] = 'done'
                            if not is_ready(ready):
                                   print('>>>ok come back later when you have prepared')
                                   print('==============================================','\n')
                                   participants[name]['status'] = 'attempted'
                            else:
                                   pass
                            participants[name]['answered_r'] = True
                     if len(ready) == 0 or is_ready(ready) == 'no response':
                            print('>>> computer cant recognize what you want to say')
                            repeated_r = 0
                            #ask 3 times for if the participant is ready or not and disqualifies if participant does not answer
                            while repeated_r < ask_ready_tol:        
                                   ready = input('->plz tell whether your are ready or not :')
                                   if len(ready) > 0 and not is_ready(ready) == 'no response':
                                          if is_ready(ready):
                                                 print('>>> finally you made a descision')
                                                 participants[name]['status'] = 'in_quiz'
                                                 start_quiz(name, participated+1,  participants[name])
                                                 time.sleep(2.5)
                                                 participated += 1
                                                 participants[name]['status'] = 'done'
                                                 participant[name]['answered_r'] = True
                                                 break
                                          if not is_ready(ready):
                                                 print('>>> ok come back later when you have prepared')
                                                 participants[name]['status'] = 'attempted'
                                                 participants[name]['answered_r'] = True
                                                 break  
                                   else:
                                          repeated_r += 1
                            if not participants[name]['answered_r']:
                                   print('>>> computer was not able to recognise your recognise your response','\n'+'after many attempts, so you will not be able to participate','\n')
                                   participants[name]['is_disqualified'] = True

# =================================== STARTS THE MAIN PROGRAM =======================================                                                                                                        
if __name__ == '__main__':
       main()
# ==================================       
print('\n\n\n\n')
time.sleep(5)
print("->all participant's performance have been added to the table in MySQL Database.",'\n')
print("->type ' select*from question; ' command to get the answer all question you may skipped or gave wrong answer.",'\n')
print("->type ' select*from quyiz_stats; ' command to know the performance of each participant.",'\n')
insert_data()
insert_data_txt()
delay = input('->press enter to exit')
