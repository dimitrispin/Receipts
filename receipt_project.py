AfmList = []
#List with products sorted on alphabetical order
ProductList = []
#Dictionary connecting Afms with Products based on their total price
Prices = {}

###The Menu with 4 choices
def Menu():
    x = ""
    while x != "4":
        print("""
      1.read new input file
      2.print statistics for a specific product
      3.print statistics for a specific AFM
      4.Exit the program
      """)
        x = input("What would you like to do? ")
        if x == "1":
            OpenFile()
        elif x == "2":
            ProductStats()
        elif x == "3":
            AfmStats()
        elif x == "4":
            return
        else:
            print("\n Not Valid Choice Try again")

#This function is used for cases of an invalid receipt 
#The program goes through the invalid receipt and until it reaches the line with only '-'
def invalidReceipt(arxeio):
    x = arxeio.readline()           
    while x.count("-") != len(x)-1 :
        x = arxeio.readline()

#Read line by line until the end of Receipt where it reurns false
#If invalid return None else return AFM, Products of Receipt and their total prices 
def newReceipt(arxeio):
    x = arxeio.readline()
    if x.count("-")== len(x)-1: 
        return newReceipt(arxeio)
    if x == '':
        return False
    
    x = x.split(":") 
    if not x[0].startswith("ΑΦΜ"):#The Receipt must start with ΑΦΜ and its 10digit number
        invalidReceipt(arxeio)
        return None
    x[1] = x[1].strip() #Keeps just the number
    if not (len(x[1]) == 10 and x[1].isdigit()): #If length is not 10 digits
        invalidReceipt(arxeio)        
        return None
    afm = x[1] #The AFM is OK
    
    sumPrices = 0 #Sum of prices of products of the receipt
    totalPrice = -1 #A starting value for the case we dont find word ΣΥΝΟΛΟ in the Receipt
    products = [] #List of Products for the Receipt
    productFees = [] #List with the Fees of the products the Receipt has in it
    x = arxeio.readline()
    while x.count("-") != len(x)-1 : #Case we haven't reached the end of receipt
        x = x.split(":")
        if x[0].startswith("ΣΥΝΟΛΟ"): #Case ΣΥΝΟΛΟ in myline
            totalPrice = float(x[1].strip()) 
            if totalPrice != sumPrices:
                invalidReceipt(arxeio)
                return None
        else: #Case we have a product in myline
            product = x[0].strip().upper()
            values = list(filter(None, x[1].strip().split("\t"))) #Create a list with the 3 values of each product
            if len(values) != 3: #Case we dont have 3 values for the product in myline
                invalidReceipt(arxeio)
                return None
            quantity = int(values[0])
            price = float(values[1])
            subtotal = float(values[2])
            if round(quantity*price,2) != subtotal: #Case the subtotal doesnt match the quantity*price
                invalidReceipt(arxeio)
                return None
            sumPrices = round(sumPrices + subtotal,2)
            # Check if the product has already been inserted in our products list
            try:
                # If the product has already been inserted just add the price fee for the current product
                i = products.index(product) 
                productFees[i] = productFees[i] + subtotal
            except: # The product has not been inserted in the list with products for the current receipt
                products = products + [product] 
                productFees = productFees + [subtotal]
        x = arxeio.readline()
    if totalPrice == -1: #Case ΣΥΝΟΛΟ was not found in the current Receipt
        invalidReceipt(arxeio)
        return None
    return afm,products,productFees

#This function sorts any given List (in our case either the AfmList based on their numerical values or the ProductList alphabetically)
def sortTheLists(list,afp):
    i = 0
    for x in list:
        if x > afp:
            break
        else:
            i = i+1
    list.insert(i,afp)

#This function is used to insert a Valid Receipt's fields into the AfmList,ProductList and the correlation Dictionary
def validReceipt(afm, products, productFees):

    if not afm in AfmList: #Case Afm not in our AfmList
       sortTheLists(AfmList,afm) #Call to insert the Afm in the AfmList (sorted)
    #We loop through the products of this Receipt    
    for p in range(len(products)): 
        if not products[p] in ProductList: #Case product doesnt exist in our ProductList
            sortTheLists(ProductList,products[p])  #Call to insert the product in the ProductList (sorted)      
            Prices[(afm,products[p])] = productFees[p] #Makes the correlation based on the fee
        elif (afm,products[p]) in Prices.keys(): #Case the correlation already exists, adds the extra fee
            Prices[(afm,products[p])] = round(Prices[(afm,products[p])] + productFees[p],2)
        else: #Case product is in ProductList but no previous correlation between this product and AFM 
            Prices[(afm,products[p])] = productFees[p]
    return

#This function is to open a file and check its content through newReceipt Function and if valid add it with ValidReceipt
def OpenFile():
    filename = input('Enter file name:')
    try:
        arxeio = open(filename, "r", encoding="utf-8")
    except:
        return
        
    x = newReceipt(arxeio)
    while x != False:
        if x != None:
            validReceipt(x[0], x[1],x[2])
        x = newReceipt(arxeio)        
    arxeio.close()
    return

#This Function for a given Product name searches through the ProductList 
#If the product exists it searches for correlations with AFMs and prints them
def ProductStats():
    product = input('Give a specific Product:')
    product = product.upper()
    if not product in ProductList:
        return
    for x in AfmList:
        if (x,product) in Prices.keys():
            print(x,Prices[(x,product)])
    return

#This Function for a given Afm number searches through the AfmList 
#If the afm exists it searches for correlations with Products and prints them and their prices
def AfmStats():
    afm = input('Give an AFM:')
    if not afm in AfmList:
        return
    for x in ProductList:
        if (afm,x) in Prices.keys():        
            print(x,Prices[(afm,x)])
    return
