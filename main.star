my_dict :dict[:int, :int] = {
    1: 2
}

def minus (a :int, b :int, c :int) :int {
    return a - b - c
}

myvar :str = "The quick \"little\" fox jumped over the 'lazy' brown dog"

myarr :list[:int] = [1, 2, 3, 4]

if 1 > 0 and 1 > 0 {
    output("1")
    output("1 won!")
} elif 0 > -1 {
    output("-1")
} else {
    output("None")
}

mysupernestedtype :constant[:dict[:int, :list[:int]]] = {
    1 : [1, 2, 3]
}

def main (args :list[:str]) :null {
    output("Hi")

    # Foobars are healthy

    mylist :list[:int] = [1,2,3,4,5,6,7,8,9]

    for num in mylist {
        output(num)
    }
}

num :int = 1

while num < 10 {
    num = num + 1
}
