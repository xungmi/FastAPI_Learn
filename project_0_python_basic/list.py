list = [1,2,3]
list.append(4)
list.append(4)
list.append("a")
list[0] = 10
list.remove(2)


print(list)
#ordered, mutable, allows duplicates, indexed, allows different data types
#and can be nested


# ex
list = ["duck", "dog", "cat", "tiger", "bird"]
list.pop(3) # remove the element at index 3
list.append("tiger") # add the element "tiger" to the end of the list
list.remove("duck") # remove the element "duck" from the list
for x in list:
    print(x)

print(list[0:3])




