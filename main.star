my_dict :dict[:int, :int] = {
    1: 0,
    2: 2,
    3: 3
}

def minusfunc (a :int, b :int, c :int) :int {
    return a - b - c
}

myvar :str = "The quick \"little\" fox jumped over the 'lazy' brown dog"

mvar :null = null  # lol this is useless

myconstant :constant[:str] = "I am a constant!!! I'm permantent :D"


def main (args :list[:str]) :null {
    output("Hi")

    # Foobars are healthy;

    mylist :list[:int] = [1,2,3,4,5,6,7,8,9]

    for num in mylist {
        output(num)
    }
}
