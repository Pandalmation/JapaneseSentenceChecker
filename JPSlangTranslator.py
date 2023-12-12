import tkinter as tk
from ply import lex, yacc
from  JPDictionary import japanese_to_english

#Tokens for the Japanese Grammar
tokens = (
    'SUBJECT',
    'PARTICLE',
    'END',
    'BELONGING',
    'OBJECT',
    'ADJECTIVE',
)

#Regular expressions for tokens
def t_SUBJECT(t):
    r'私|僕|俺|彼女|彼|君|貴方|あなた|私たち|僕たち|彼女たち|皆さん|犬|猫|男の人|女の人|友達|警察|学生|ジョジョ|パンダール'
    return t

def t_PARTICLE(t):
    r'は|が'
    return t

def t_END(t):
    r'です'
    return t

def t_BELONGING(t):
    r'の'
    return t

def t_OBJECT(t):
    r'鞄|眼鏡|傘|料理|名前|人|町|学校|時間|家|食事|花|夢|自然|勉強|本|動物|天気|街|音楽|海|風|言葉|未来|青空|心|水|お土産|雑誌|牛肉|星|仕事'
    return t

def t_ADJECTIVE(t):
    r'ヤバい|キモイ|きもい|ウザイ|ハズイ|むずい|おもろい|ウマい|イケてる|キラキラ|カッコいい|かっこいい|グロい|キツい'
    return t

#Ignored characters
t_ignore = ' \t\n'

#Parsing Grammar for N5 Japanese sentence
def p_sentence(p):
    '''sentence : SUBJECT BELONGING OBJECT PARTICLE ADJECTIVE END
                | SUBJECT PARTICLE ADJECTIVE END
                | SUBJECT PARTICLE SUBJECT END
                | SUBJECT BELONGING OBJECT END
                | OBJECT PARTICLE ADJECTIVE END
                | SUBJECT BELONGING OBJECT PARTICLE SUBJECT END '''
    
    #Displays the header for the parsed sentence in the result_text widget
    result_text.insert(tk.END, "\nParsed sentence:\n")
    
    #Displays the Subject of the sentence
    result_text.insert(tk.END, f"Subject: {p[1]}")
    
    #Translates the subject to English and display it if available
    subject_translation = japanese_to_english.get(p[1])
    if subject_translation:
        result_text.insert(tk.END, f" (Translation: {subject_translation})\n")
    else:
        result_text.insert(tk.END, "\n")

    #Checks for different sentence structures based on the number of tokens in the parsed result
    if len(p) > 2 and p[2] == 'の':
        #Displays the Belonging and Object components of the sentence
        result_text.insert(tk.END, f"Belonging: {p[2]}\n")
        result_text.insert(tk.END, f"Object: {p[3]}")

        #Translates the object to english and display it if available
        object_translation = japanese_to_english.get(p[3])
        if object_translation:
            result_text.insert(tk.END, f" (Translation: {object_translation})\n")
        else:
            result_text.insert(tk.END, "\n")

        #Checks for additional particles and adjectives
        if len(p) > 4:
            if p[4] == 'は':
                #Display the particle component if it exists
                result_text.insert(tk.END, f"Particle: {p[4]}\n")
                
                #Check for an adjective and display it with its english meaning if available
                if len(p) > 5:
                    adjective = p[5]
                    slang_word = japanese_to_english.get(adjective)
                    if slang_word:
                        result_text.insert(tk.END, f"Adjective: {adjective} (Translation: {slang_word})\n")
                    else:
                        result_text.insert(tk.END, f"Subject: {adjective}\n")
                    
                    #Checks for the 'End' component and display if it's there
                    if len(p) > 6:
                        result_text.insert(tk.END, f"End: {p[6]}\n")
            else:
                #Displays the 'End' component aka the です
                result_text.insert(tk.END, f"End: {p[4]}\n")
        result_text.insert(tk.END, "\n")
    elif len(p) > 3:
        #Displays the Particle component
        result_text.insert(tk.END, f"Particle: {p[2]}\n")
        
        #Same thing with the adjective component and translate it if available
        adjective = p[3]
        slang_word = japanese_to_english.get(adjective)
        if slang_word:
            result_text.insert(tk.END, f"Adjective: {adjective} (Translation: {slang_word})\n")
        else:
            result_text.insert(tk.END, f"Subject: {adjective}\n")
        
        #Check again for the 'End' component and display it
        if len(p) > 4:
            result_text.insert(tk.END, f"End: {p[4]}\n")
        result_text.insert(tk.END, "\n")

#Error handling
def t_error(t):
    error_message = f"Lexical error: Illegal character '{t.value[0]}' at position {t.lexpos}"
    result_text.insert(tk.END, error_message + "\n")
    t.lexer.skip(1)

def p_error(p):
    if p:
        error_message = f"Syntax error at line {p.lineno},\nposition {p.lexpos}: Unexpected token '{p.value}'\nPlease make sure the sentence is complete before ending with です" 
    else:
        error_message = "Syntax error: Unexpected end of input.\nPlease make sure your sentence is complete\nand ends with です"
    
    result_text.insert(tk.END, error_message + "\n")

lexer = lex.lex()
parser = yacc.yacc()

def translate_input():
    input_text = input_entry.get("1.0", tk.END)
    result_text.delete("1.0", tk.END)
    parser.parse(input_text, lexer=lexer)

#GUI using tkinter hehe
root = tk.Tk()
root.title("Japanese Slang Translator")
root.configure(bg='#ffcccc')  

input_label = tk.Label(root, text="Enter Japanese sentence:", bg='#ffcccc') 
input_label.pack()

input_entry = tk.Text(root, height=3, width=50)
input_entry.pack()

translate_button = tk.Button(root, text="Translate", command=translate_input, bg='#ff6666') 
translate_button.pack()

result_label = tk.Label(root, text="Translation:", bg='#ffcccc') 
result_label.pack()

result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()

#That is all! ^w^ 
#Japanese Slang Translator Program 
#By: Tiffany and Jocelin
