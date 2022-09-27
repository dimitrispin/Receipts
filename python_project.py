LAB21142999/                                                                                        0000775 0001750 0001750 00000000000 13570264165 011770  5                                                                                                    ustar   tinyos                          tinyos                                                                                                                                                                                                                 LAB21142999/computeSales.py                                                                         0000664 0001750 0001750 00000014357 13570257176 015024  0                                                                                                    ustar   tinyos                          tinyos                                                                                                                                                                                                                 #List with afms sorted from low to high
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

Menu()                                                                                                                                                                                                                                                                                 LAB21142999/report.pdf                                                                              0000664 0001750 0001750 00000400617 13570262246 014004  0                                                                                                    ustar   tinyos                          tinyos                                                                                                                                                                                                                 %PDF-1.7
%����
1 0 obj
<</Type/Catalog/Pages 2 0 R/Lang(el-GR) /StructTreeRoot 22 0 R/MarkInfo<</Marked true>>/Metadata 70 0 R/ViewerPreferences 71 0 R>>
endobj
2 0 obj
<</Type/Pages/Count 3/Kids[ 3 0 R 14 0 R 16 0 R] >>
endobj
3 0 obj
<</Type/Page/Parent 2 0 R/Resources<</Font<</F1 5 0 R/F2 12 0 R>>/ExtGState<</GS10 10 0 R/GS11 11 0 R>>/ProcSet[/PDF/Text/ImageB/ImageC/ImageI] >>/MediaBox[ 0 0 595.32 841.92] /Contents 4 0 R/Group<</Type/Group/S/Transparency/CS/DeviceRGB>>/Tabs/S/StructParents 0>>
endobj
4 0 obj
<</Filter/FlateDecode/Length 5117>>
stream
x��]Yo#�~���Gʈf�> ��H�N�8qlA`�ac���5�����������X�"�3�u�Wխͻo6�>��!��f<l�s{C&��3F��H+'�6F�ɲͯno�����������݉n����<���W��{ǚ�ȍ�jR���e_~G������\��1����ͯ?������~y{��a�&h�y�i���{����W�	z��c����͓��/�7�^�mVÔ��[���a9�"p��K"�������}u�7�vb��5~���5m��>l6����������q��������]�)(�M�^M�7wb������^l�z��l{���gtAU��r��]���=��D���Q�,IKb��;��N�{>۩|		��.�]����p�g�|������w�����M���BMZ,l�U����5dZ�m���l��̍�j�A;���|�z`�k��/�5fﮡ����dw��eny�);��O�����{���)��t�o=����7
�].c2�l�y.�91c���3O�"?U�摷��F3�=�~#��C���䯍��}[���p�d!Y�+D�T�ڲr1h�,�(u����&Y(������5b��&���b�V缴�Ȕ=d5�b�����\����>�)�|�8���^�8�=#�Ge�d�bc�ם��i�@�m�� U���[_�f��l2AÃ������{�\g��Zd�Σ�<�A;iu0��M}�6���Ԏ�p���h��}t�D�ܙ��a��f���<EL�	�?�Y�W���v���KC�]&�R�̕|���_?�Q����s�W�1(-��ۍ��$a^(cF�ⓤQ��P��:c��t}<�#٤0���I%�Q.	��q�D�/1���
�E�Ib��9�G%'�Q�]�7m{�u��{y���@g�o��]���xo�2�i�G��f�2�t���n�>yU�O{Ȟ5�,�o�E=&�CkXOp��^o�M�Ei�"�����)fh��NO��M"Ŏ�3����  !��C��>�e�aa�k���G�CR��h�W��\���t�ac>W�芓�D��(��d�̒H-�)�UQ-|m��+kY��SI�ˤ**�
� ewm�A�.�bM�s�p32�7k|�\K��'i9�J�ώT�\���X|K�f����$O�JS��-���)�#�0��/#�S��Ex,����.�h��4���h��M\���o3���!8*����:4�.] k8��^	F'�g�k�v��S����MG!��|,m�\�	#&���
�(Y��j���u�6X�]��J�UR�(���%�5�T��?�[ZL�Sl*��K@X�:c��-ه��X�5j}U"�G4��d�1���	;�\������>n&�Ձ�5b���qTې,$'H��Sc<r�S�X���9�ہ������������[W!�#���b����:���'�62�V��ؘkD�;��TF�z6dbԥ��ƪ���.$�8j�t�+'3l��h����q(� =W�d��e��11˃Y�l]��ܪ&bq	
(��g��|��Y*{�̵�1��l��J�x�.XZ��s~L���q�	�@��ӃMP�5�^i���6_R��Z�R����AМ"َ���H�X,�w��G����G�2�qyQhz}cb���e���0�
Ecl_L��X�߽�M7>�1����Z�橫�BY[R�S�0lMg� �k����p�*f��[6����R��d��h���E:O�֝�����zC;8�OS�����k���s�F����L}��/
Ԃ��$�?�95N|7��(��B��c.k�X�  �i�F��B
�ˁ"7*�šG޶(VY�x��5�����E�EjzY>��!c���	�����b*NX*������4�/���ʆ�T����0c���6e:�*���Tyx���1e= �9*�M:����T���V,U�8�BK�<� _r,��PT��WsI>Z驝����"�K��T�~�L��E%D�:�bq����_+ڔ����%}M�*FU+z�n*�Hv-�i[ӯ�G.9"�u��zB]ӷ�ȁ���E�k�T�"lAU�eNHi������Zc��c1�'�G2�(�\�g,*�$�t�4E�T�$1H
ӕ-p�eѕá���������,����qi����S���/5�{g,�?0�w˂XU���p�7G\/D�G/��1a��㽜c=��u��%!���ɏq�1W~j&GJ��!H9E�9�&�Y����Ƨ6�n;�&��؇Q�p��g�0�^r��y������cC(.''_k���F)��HF=��	I��[	�%��)Fi��s����k�[��,��3��Wٞ�ޟ2P�ٱ��K�G�T��W�V�
Ց=��9$4a)NJ��o������,��{x�6�#Co�q�KD�5��ѽ4�t���J3 !V?�wN ��
��k!'Q��!�`hO@C<q
Q��7.`����D��9%�8����0����Z��G�1�����&ݨ����I���`������ͰF�D�Z�&����^?�sv��O�R�?�mΞ#��%��ƍ�|/ꗭ ��ig���Z�jÝ�>��X�Qu"�>�r���q��+H��fuRb j��x(�MD�X����U�*��)�����#��4+��++ �\BcLy�u��.Oj\�
%��C�eqT��$k�(�~T��K J�X�0�������P�^ZW��)����zԩa�2�y��(�3D�C&���uh�t��	!6���0汱Z��\>��N�-EY��~�)�/����l7��z���UI���5v�&��r�j^j*v8�W������f�`�n!5�o��q�[x��3����y�-�C�5����� �鐘���#�NJ�J["5�A߂7E�jS�fI�K����E�b��U;0béD��n�\�A�l��b�0hM��d�JX��;�Q�P33ط̚���DD��ګ8p xJ���x��2���Ō
O;>��z�_n�ڏ��_cl�7b2F��\�/s�M�Q�C4�w�>��\[�\Maϻ�c����3��$��I)����Gm�0W	?�O|��r�Y~ˤL$��wK�} ��,����)�E� ���qG����wXm�$�8B{���Fn'�7��ǜ�%I��&ɩ�l����nH�U'��="@Ǎ+��.m�SMK/�P�Ju�1�HP���7��ǩVH���{Og�Ү"#=��:�@���:��s�O�VD�i�$X=�2x�'0�� >kz2�K�а�#����C���bx�� �eJGjW(���~ eLN.X�_h�;8�bm�v�_ԭ�H�K�l�i��S��+��=81w��8��3q�h���tT8>�bs�n�u:�'���=4 \��-��	v�aW`N� ���.:ӊh�{�hW�`9�&�/��)Q8cJ��(JI5���i��;<x��U�������95e2�K���5�0?M}�2�eZ~b��([|>)��3gF �1��z0�����n������k�L$�qȒ��;x�Qy���h^���v��5*!j��K�x�̔�\NHޢ
�h 
E��.�3��HH��xsI����������!��t��ܟ�70t��o?���/�F$�7�9B���`l-����~�'�}��?�_���ұ)�/x�Q~��"�yT8Cj�G͍���w�i%2vY7
-ƷH)�f6p�:u�����II��3��Z~�O��>R�Sg/��m&F�������"��P��X�c9)��/�^��)���(3� )l7�àG�򞾼�.V�%�#_���e; 6.�������!*�%45���=��G��ӥ0-��֤k�7���=ɽ��P^R���\�ph�,���/�9���/Fu?@��A�m�Hg��]<���,{���l�2�Bƥ��d־f~���v�cc3sij5�!{�g��٥᧣�c� /�ߦ�j��1>�Pu�7:����טuk��I�|""�|���f���:9��{|u�9�k5��~lG�s��Jz�֒�i9�����`^�{� ���@�Yu�:�b� j�'�5Ǿ�/]U]\rC�[ԅ�.
�z���c����CU�G���L�s��g�-�>����Y$**ޓ����"�B��$M�dʜ���'`+N���J0v��p������Q*���*���E�^ ���~�o 1���<��ΩE��������Ĵa?l�
��~h!D0�'#{oEs�v`͂�$D������H8D�U��F��:u�D_M�h��!��Gr`|i����j(����g�&�۱�~�_�ճ����i��Z��� ��巒�e2�n�c���!��d�5\1a_&��8?��Y�c�bo+y�!鼁��-9e颚I���Uڨ�o��Xe�(a� y~��#Ȳ���?	�2���v4n�;�c�m���(�(�:/��IkDT�?z$��K�ᕧ��@ӉZ����p�Gq�Gj|�#pʟU�)� b��jZ�'i���ք�z,Ӌ��Y��I:!m��x���d���WM����
���-��w��Eݧ0L��<��5@~ќ�%O'.IE���6����T�ِT�5�A�|���dj���+��5�,�ɚj��$��T�(ue.$mL�_��@�F� ��
h�����4p��uK�|\���/�����;J�.��ήE[b���F�V8�BQiwGA_��Y�C���0v�����res�嚐`t,ՙ
3 �P�71'�ټYA�.�-�ao�%F�Ӷ[��X��>Ċ�ttg��z=t!+x1�׹���͖��1c���q2u;s�RBh������.�}l���=��f�ۃ�}!G^��Y�r��g�|���.I�[{V�[4!h���5��V3����[,�,K'l׽���nN�e5,o�fD���j�8��g�y����_-�Ҕݰ9����d�E�;Pt�*�޹#���q��oB\<�v��h\D�����.l�{��O��S�k`���1I;�zq��/�ǚ�N91v�D�:ҹ�
endstream
endobj
5 0 obj
<</Type/Font/Subtype/Type0/BaseFont/BCDEEE+Calibri/Encoding/Identity-H/DescendantFonts 6 0 R/ToUnicode 66 0 R>>
endobj
6 0 obj
[ 7 0 R] 
endobj
7 0 obj
<</BaseFont/BCDEEE+Calibri/Subtype/CIDFontType2/Type/Font/CIDToGIDMap/Identity/DW 1000/CIDSystemInfo 8 0 R/FontDescriptor 9 0 R/W 68 0 R>>
endobj
8 0 obj
<</Ordering(Identity) /Registry(Adobe) /Supplement 0>>
endobj
9 0 obj
<</Type/FontDescriptor/FontName/BCDEEE+Calibri/Flags 32/ItalicAngle 0/Ascent 750/Descent -250/CapHeight 750/AvgWidth 521/MaxWidth 1743/FontWeight 400/XHeight 250/StemV 52/FontBBox[ -503 -250 1240 750] /FontFile2 67 0 R>>
endobj
10 0 obj
<</Type/ExtGState/BM/Normal/ca 1>>
endobj
11 0 obj
<</Type/ExtGState/BM/Normal/CA 1>>
endobj
12 0 obj
<</Type/Font/Subtype/TrueType/Name/F2/BaseFont/BCDFEE+Calibri/Encoding/WinAnsiEncoding/FontDescriptor 13 0 R/FirstChar 32/LastChar 119/Widths 69 0 R>>
endobj
13 0 obj
<</Type/FontDescriptor/FontName/BCDFEE+Calibri/Flags 32/ItalicAngle 0/Ascent 750/Descent -250/CapHeight 750/AvgWidth 521/MaxWidth 1743/FontWeight 400/XHeight 250/StemV 52/FontBBox[ -503 -250 1240 750] /FontFile2 67 0 R>>
endobj
14 0 obj
<</Type/Page/Parent 2 0 R/Resources<</Font<</F2 12 0 R/F1 5 0 R>>/ExtGState<</GS10 10 0 R/GS11 11 0 R>>/ProcSet[/PDF/Text/ImageB/ImageC/ImageI] >>/MediaBox[ 0 0 595.32 841.92] /Contents 15 0 R/Group<</Type/Group/S/Transparency/CS/DeviceRGB>>/Tabs/S/StructParents 1>>
endobj
15 0 obj
<</Filter/FlateDecode/Length 4414>>
stream
x��]Y��~_`�C?��o6�� ;3;A�H`y0� �k�@�8������c��S+�t7��u~U���ix||������N��z�uF��L���#F�D�(����������������� ������;u5� �8#������~��O_䳇��������?�����Y>���w��a����#.������$B�W��?˟���bX��|:b�5��/�/П�Gu��J������w�o�s��	�?�O�� ��z���:Ȭ+��Nԑrs��?���zI��J�qQwȅ���ns��5O<�uiN��h����G�'C z�K����e���o�/�Ϻ8b�ױ��t:��87�Wפq�ĳ�f1�f�D`�B#-��f�{-�#4e�y��%�]w���{�d��/�e��rnϷ{��P��H>1>���_?|�z����ç���˧�_�{hg!c#�ef~�� ��?Gr�������&� �BX�J%#�&������8����>|]�mgI1����4+uNl��ٲ�Ȕ�z�蒶>��fM�ي��<��xŎ�	h�1WJM[P�^��QL%�2ڭm�j��#�E?���l�/��9Δy0&\�c&��5��r�����H�����RYߠo�:�Ӧ<A��~
5Fӹ�Klӈߓ�����3\g��̛���rc���g��d>'@n^y�,ןkS|3�4~�?��ݬ٨TnF�/�>6�َ�	+Jh�%��>
@ַ�\mF�L��T��+x�脍��qL�8q0K	�o�a ^vˑ�ڈ8���N�T m;���(�Jt5kh=F{�d�|啜�!�H������Y;M�Bh#��`^n�&��sW��B�KI4]��5i<���)�R<v@��}K��8�lc	�+j7�h��-�pWY����id��$�5O�e�`c�*�"ڀԷD�$D�}1a��/!1�!���ȍ^�%�(�,Z�y����Ԣ�lo�� d<�f�'������$�Z�_C��l���mȥ��g�j����mwf)J@��}^I� �����%��b}Hk��ȋ��4q8�ھna���,�G�j��Ɍ`C:B��]�����K�eV��|A�er��r��]mB#�~��:3���W��8-�?���舽��ҔZ]S���I�S�
�Rޚ�A7�k��c�Y�����Zz`��I4!`�jz�I�'~v�X7�����+D��>��f��F},X�2���PŋZDm� ��>�`"r��">�0�cQ$&GRzP��G"Q>�r~as�4H����O�)�`�H$��&�(`eo���x���@�a���lp��b
H�P�����G�jW�,iG����M㛬Ry=2��yC�ՙ$h�*c���c��?%ŧ�����ize�5;ԛ��!��iO0yC��3�5��(�ԋ]��e��iѐ*�F�7�E8��8ՄF���j���s���}!Sy���W��p�RqYAu(�+y�Okh����/=�ڞ��	;WT�,aI.�8S��=�E�P)�yn���"�~Z��l���>���pXaYә�>.��3��Z9���,�w�2K&� �Gb��<����Fћ�Ŝ�;V8I&�.-��E3���h���{�g#l :m�X�B4V�n�e_��p����`�ʦ�"M��B�w�z�@�G�*�}����v@.�7��W� ���9˄���|��ƧW�EzT'�ƨ&Șt+ѝ�㍵�YU x�܄F~�}TqdQ��*તzW�"T�j�SSv�%~=����tqp��t!�v����<���gm_����zG�,x�y�9J\�Y��֙�@1P���-T2Hy���I�UW�u��-p��w
@�q�i8�4��=��J���$od���"W�M\���э� L��t!�G�K"dD�4�l���a��۾�3]��{�s��5I!�L{K)�잵��4��K8��8��Ygv,�%K�'��Ek�@m/�{��;��'$
��P��l�����˿W#��P!bD�-��U
G>�(������U��Ʃ�G\{�R��/Թ��%��L+F#-�ay�R<�j<�N/iD�6�V�Y�Nl�ľ�=,\�	�$/�5YBn}M^ RF7I�d�U�8����_��y�N!̓����&v<z�O����8�G�΂�Y��Mʙ���/�;�J��B^���JL�j��ݾʷ6e����+�e({��������IԖ�1"� ,�Yu�7YEq|����șҴ��Kc(ո�g�Q>]>��G�W���u���$@T�����2�����1X!��掇Z!����;;������W���ܞ7T:����P��E{u�l7�j6V;��XQg/tf�:�x!�:2/�m7�/q��f�aq���!;E� ��ӌ^Q"�e�B���`����5W��W��R�w�Q�)��nM��O���&��iޞ��� 6�b��F܆4�������5��@�����86�D5Tn�T����>땭�����&�Ib4�/���D%�P�@�Ċ�pM�!���6��PmW���1��U�L}{�,0�����9��T�vVj�	d_��20�Lx��>�����À'�j�t'���[���lB�V��1��$0Qe�w
.�?�ȄU3�6����Wv�-).c�Q���y�d�W[��:
1�i�w���Ot�Ql�E���nh$�Fَ�>~�W�`T����m �#��e����������|���m�E�X�lce�4z�#��ߠL#U�a�P�H'Q�Jn���$F!R@�,�Wj�7�����2�ۺju�Y��SPw�.,>�S���8kG�S���M��i�EVs���Ѱ�%[[r��љ��"N��ufb?_����oC�3����w�Pgҗ��c}B�F T\�J
�9����<�bGҏR���k&��!@�6��Flq����+Y�����,��S8x�V���a�̘q��)UA_�9y:Q��6���L�%"k�Pl���]�f�\�W��AIɁgwhK4�?�O�� y�����jm��6�9���l������t�C�v�sW��(�Y\�4��Ql���oB�TAf�4Fr?�I5#Dn ����R5+�T�e�M���Y�L
�U��_=�u�i�K1cD����Ě��
�jk�J��d�B���I��~�@jڷ̰|��W��XUQ�̍�Y#7���Mi�_9c���X�M]���k@cPA�J�#!I(�8n�~~�Hڝ��*�!O0����h����.�t�OT)b@�N������Ĵ���tأ\u=Ͷ�5X<i8���p��-��Jѱ��Ĭ/_?|}���D�afN S>`�A-�p(T@^2��w��6cN�^`�
�Oq��+NĪ�>'y�)�XS{c#���
���%B�*�(�E���tl�N.�e�V��+�O'�вX��h��ӈ���S�u��_C��saj4���!��Wt�Os9Um�7$�U��,�ݒ��!.�,mX�|��f/ն�2�(B�`����IFS�6�spn�ِ��%ƳƦl���죣��R�O����a�c�rSʝ4�c� �IY��w6|a����������7_@�4@���A�C*��w��=�p�F1,��lK��^Nc&��[1�q��;�R�mkϒ�*�fa,
	�Ι.�a�=�e�HA��xح�a�������h<�&W���gQ~�u� W׬����r��;a_����I������W�,m9D3o�{��1FZ�kq����dM'�en�#�e�a��(���\�uI1�S˥{�9�Ҝn���E�B���OϢt���[82�����s����Jz�����t�
��+�rfAo��Mug\��\i&��W��ŕ�m�m�`�LWy?����I��;1'� ���m��h��N5@x��/_?<��jm�6���bRW�2�I�>Ԡv�
�n�>�C��"�� �d$�c<�8U-Ŭ7�E��`I7x�1�Ϣ�\ve���y4�!�,�/�/���z6{THN�@� �O+�Dm2R0�t$�=�f���R%�&?�L�!�7�ʳC=�Bkg9�c�r�2�|�f��wXXHNWeϙK+�Qԡw�M��ȇ�"���S";N�0�D6R	
�D{����ʢX̧��Ne�?�*�{��W���Vc`d��3��Z����c��dCp��[N�	b��v4F�N��RZn�;Q�����;6L��5�>����tC�q�=�����Bk�X���]AH�3ά�+�a��mj�cO��D�����"�a����^N4<`�����q�a��#�hX"��UN���
endstream
endobj
16 0 obj
<</Type/Page/Parent 2 0 R/Resources<</Font<</F1 5 0 R/F2 12 0 R>>/ExtGState<</GS10 10 0 R/GS11 11 0 R>>/XObject<</Image18 18 0 R/Image19 19 0 R/Image20 20 0 R>>/ProcSet[/PDF/Text/ImageB/ImageC/ImageI] >>/MediaBox[ 0 0 595.32 841.92] /Contents 17 0 R/Group<</Type/Group/S/Transparency/CS/DeviceRGB>>/Tabs/S/StructParents 2>>
endobj
17 0 obj
<</Filter/FlateDecode/Length 413>>
stream
x���Mk#1�����*�e��I��B�e{X��,mN�e��V'�Ni3 F�e=��b`v���ny�W+,VK�k�Cמ��)��!����њo��ۚ�ښ�� �'kZ���|�$C����]%�Z6}I��5��.���N����Dm��5�,W/zZ%];�[�ضb�h)��B!n�nO�j\s���;��v"*Q��7�}�����R;�`�	:糠�q�~�v)}
�'�K:��gox���zJ*z>���yO�����`4\����+NPD��[�SJ�I�'� .�V8B�\F:��t����1�c4�H�Pw�/)��4<�tN��<ï�[�y��y��?0ŉcN(	S�qH�M����$q	)�I�)�I��D���1K#�kT��ݘ��b�
endstream
endobj
18 0 obj
<</Type/XObject/Subtype/Image/Width 783/Height 168/ColorSpace/DeviceRGB/BitsPerComponent 8/Interpolate false/Filter/FlateDecode/Length 11818>>
stream
x���[Wچ�����f��L2��囙d�ϙD'&�1�d��dC�1.QQل�nYz�޷?ꫳU����nP�������uy�9�y_�                                                                                                                                                                     l+UΆFB������$&j\-���������~��8[�w�����Ҍ~�o�H6�,��T�p[9HI����n{    � Yr�Z;/y�ϕ?�v3�d����,N�ʒ��c�e/d	   �CEU���J6�N����������u�)Kԕ�����K�>�   ��I�Th��di��Y
X�JE�,   �TVל�N��y�;�MY��u�̦��;{<��%��Jܵ�yd��dR�[�h�W[����&{z��Mk���;���:�ё@�ɽ#��م�dd����S�7�/��q��/x�����6ܩ����W����YBY���v���������G�.z����Ur���������ݣ��������j�Sc�����6������p6��*N}���Z��/L�M���Nyd��}���+צ.��   �VJ�%S�(Q$bG�Ց���\]�'��u���;2�_�q֟y������G�R�S�(E�'{��%"C�=�A����tޛ�F�����'o�6)�/�>����`�O��ؐ%��M�=9�D4J(R}�*M����I*K԰���!Պ�UiJRC�'K^%��,5����U�l2�$ySc�>Ոl�RS�K���b?)qR��[�/  ص�!K�tb�6ό�-�"�	�BN��.��;�)$*�J9S)���Ǿd� yh�D�(�U�>1;���i�0Ce���z�o����ÑEߢ��<�,1;�[�Psb��M�~VS�M�%A�e��d��J�J����@h���%=   �bP�,�T�@�+��u��̦�+�r�)ҟM�T�,uW�e�ٕ�s.rο2���H��Ñ9o6El�K߆d)]��Ǚd)��͖.y�+s��xY�q%����@�7�0u��G   ^6I���E��%Cɒ^����Y��x����=���]�=�I�������TY���F���v�,�5���a�  `���%�5�t"<�hK�%/�^<��{�'{��O���|��m��G�,�%   `7�W�*�k+$z�v0�,�hi6׊���%mo�&K�Hyw(��5�r����g-Ko�r�����#�W_��r~Z}sah�/�`c�D*�=q�!�,Kĕ�2�,�6wD�|n�46�f�DK�
�   B>Y⮔5�R~Yb�R8mQѭm#�$��v8y3M��L8��d�m�6 e.�Z�l�5p6��w��s�ʊ�Ȓ�N}Ӣ�CM���d�FKs�R��M�%�6 �p	  ��F���)LY��(1Y⧍�Kz#�d)�O��V��.K$Q�s��و,ѷ.c�S'�.�͖�-�:�B�%�Y�k�����|�D��;�J���vғɫ����T�$�Y����4ɣ��~�'�+��   ��#�f	     h@�     
 Y    ( d	                    ��7[�ƞ��vK�l*�6t���m��,%K��]um��贴��h�s����ڿD�1��k',ξ����_���}��o���o��N�??9�[�tl��  �%��Rm��']���?k>!�݂�������푺v�JYb��P�A���O�(曺��Q�N����7����~�Y�  ;co��t���A�ʡ�,m!ԕ�`�k��>}�������~�� Y �R �4J�ߡ�TYS{vv'�d��Be)�\�(T�|V��sd	  6@E��8]�5��������N>.����~��#s�f�w�ޯ��F�с����A�����{�ŀ���Fd�n�#�l����$φ����t0���A����'2	eQ5�Ws�`���'��C2t|�v'M�3ސ��<�r���mo��e2�|O��ޥ����3�s'�Z�_���p�����y�ϫ����>~:Z�]|j\}�OƵ������k�[������*�t����h�ރ�t�=�?�?��s�{S\����&"�ewϛ�-�_~���e�?}�r�/��+�O�Κ$kY����$v����;_���E�]���W�,�5����'V�n���E)ea�ߐs{_�ōy�ݭO~q���F��/�v��ΦB���F�k���A���QYj~��&�WG5o���_�\�����ځ��\��DV�_����_�g*��_o*����W�4  x(E��?�|�.��NF���_�H��uGF�Tx�vy����5����[S�:�I�t�H��P]/�Kߺ�L�	�����������oZ.x�/���%}��~��RRkK���v֭��-�,�Z;/yͲ�DIW�ƶ��{�u#9�Ԇ�6���-�KM�cr����)%m�n]����Kdi^R����'ƕ������p�t87"��e��+v|����k�����sCT��,Q�fo���h{�5���Z}�#�M�>U�͗��H%M�Tqz����quN����o\[��E��:^�ɵy�,1Q��OrE�|���+�u�����}#�����k�5�!�HM��CE���R*���镟���FWݽ��%4��@R�TX�ț�L���w_䯑, v+UdN5�_��%nJ�����%*K�t|��;���P8<�]�O��	E���Y.ѷ��Ru}���A͕��[������R�T��w�T��ql,��Rnͷ���zJ�R)X%K��cĚ�#�O�����%&K$i�ȋ��-n��4eR��R�ރ���k�$�d��=���?Տ��DC%?W%z���?s��rZ�#fY^�����o|�з^Z�7�%nJjD>jKT���I����Ͼ�������I�{�ۮ��ü�J�e��5rneTؑ	� `WRYMJ�������Jb�-�z[K�ƿ�{yY
鮴qYb�R6���%�5K$[�lD��\�ڗJ���ē%�.W�/Y�u%E�J�jK��3Y���V �-����\<Ǘ�,�uWb��\d�}��J,M"�zl�Ҧ�RY��dɧ�˖敉��,�o�&�J����c��ݣ&W�)KE\	� ؅TVר�d���y�%O�D��Y�%C��rC����V���ʐ%�G���w��=�ߵ����`IDKSe˒�d���ت[��V}$�,Y�R?Y��]5KYbִ<�S`C�f�Y��W��6W1�lY2K"Zr�ʓ���%�% �.���*Q�Y��I�%!Gֲ�L)�b6�,�?6��L\���M�$�4���Rd��d�����7���L�$x�����%�/n�d%KH�  `3�L)��*�k�=*G�����<Y��k�`$��}Y��h.a���1�a����B��	�1�R����`t}����%�(a���%9�+N}?`]�dQ��bE�Em�����j��»Y�-Q*]�Z�D��rd��Ҳ�ܛ����ʽ-�oM�-S�$�s%Z��O�,l��Ҫ��{�u
�G��Y%�)�'��Ѽ����_�gj}e�B� �ɔ��:�])k�%�,U�:��p�F�X��)![r64�y�-�QWR�d�FKތ)[b��T["r$���Ñ�q�ْ�,��o� u%EJ�h�4�ɗ-Y톣�R�4�c������S��F]I)?Yr�	�Kt7�»��,�t�2/��Ă\�e8��mx�<�$�2Y2l�cm��ɖD�am)��n8AɲĲ�HZ_���N�%y3\~Y�m�B��8R�$o�#�҄��F�=Qs�2[����F���7�-ESA��g�G����% ��Tʩ툭�k�ȓ,I�=z��B�$�Y�/�������G6�,�KV�ކ�K�ϒ\����&{ɒ��Kz&bFr�%�҉K�\�dU�mh�Ĵ����XN��T�$�Y��,��pn���z���$�Y���2k��%�'.�K��%��[k ���<���6S�R�n�c�m��&r�%���'�B�,e�0,N�J�T��,����P������,9�m���m�8�K�e�$Jݪ!͈���K�oRte���/N=x�W*�xI�Y��0h�$Z.��  ���,����,���,  x�,�� d	  ���v�%   ;��	@�                    �-x��t"<���~~��Rѵ���r��f�~2��<(ڮ{���Ds����-��
o��?�f�|��V)=5u�x<�+q�	   `�Y��l8��-H��p��R��p[)K̔m)w#dɵ�Q̪�7d	  ^T�-�����w���rxd����2�+)��G��������
�h�?�?�Q���3��[���p4���Yt�	k�Շ��'�l���}��
  ��ʚZ՜v�/A��-yǝ #�g�m.ĕfe��ĊdKT�|�N���l8ժ K  ��TT׼?���YB�,��;{<��m��pd6ܬ�������j_a:)N���;�=�w���!W��IؙG���W\�������p��l8�t81DW��͹�����e��t	���+�]�@8��L��?d�K���I�����.�D��]G!Y��å�]��U����@?moR�<��]A��W�)oi6E���,�מ����UϹ��pl���j���tKy8��g��=HW�bJ��R��p6f�Q�+�?�{��_ȶ�O�T7R?�M������lp�799Y �ͥY"���YcJ1<W{M��`�TY[wdDI�Wni��8������"6V�����!1X��d�٠��>>��j<3At��͓,�56��X���r�����I�����FY�����mhn;�&���N�\����fYb��+Rc[[�=�������6���-�KM��9�����)�tl�5���}'�>L�ҕ��c��q%�0u���9-]΍?j�w�ʂ_�����m����%m�n�5�l{�5��ڤ�N�o��ڤh��~�G�(i������׮}�e��o\��d����-~Q�⥎W~rm�,KL�b�\�:_}��Jq]���7bG�-�����_\�\���뿼<�s�g''�ž  �m*�TURl��1YJ�-��G�CԖ�,e��[��sĖB��vy>YJ'aGĖfi�Dߖ.K���G�5W2co�&J�nK��RMS�ǣA͕̔.K�-���)��|;[:����+��U���9F�I;���[�-L]b�D����ȉ�R`a�v	�JS&��-��=��	��JL��zWHKoU�h���DO]��g�"^N�vd�,K���p��x�����K���\�����y�n��,���/T[R�Iu��S�@�  `s`�ėn��J��q'l�-�z[K���B�#K!ݕ6.K,Y�fS־d�f�dK��ȒX�KZ�RɲT��x�D��J�%Y����XISmI5�~&K��
@�����_����R��-�Ef��̮��$r�ǆ+m�,m�+�lɢ�;Jԉ�,͐z%��6�D}n��  �M��
��A�<]�?�fI�W�%K��ɒ��KZISP_�+C��9җ�"�ٺ��[|׆j�r�%--,L�-K����h��U�5Kֲ�O��rW��D��5-���жY�D����#��UL�!�4�,u�������ѵ	�N��%M�����߰"����/  P�K�l�9�%��4_rd-K̔R1��)v`�ɒ�c3i��u_��dI�K�]_*E��O��)��x�_��dI�W)q_*)Y���%�3����$Y �gB�,UV�V��s9�$���~���RU]�#�Dh��2,s	���Ktԕ�/N؎I�j\-���ç,���,9D	Sde�/��]q���&��%+�.jKܗl�0�P�����Rn�R����$�$�#K̕����$���U�hyw|kj�hyw�4[2�J�ɖ&&�����&}�%  x���p�ы�+��L�T]��6�=Yb�R��l���x恶�F]I��%-y3�l�mSm�ȑ�`�G��YgK��w��ԕ)Y���\&_�d��fKa�P��EF�n�ƶNi�u%��d���$�.��p
�PV���u�ʼXvrŗ������3T��dɰ���[�K$[zI�������%�˖"i})��n8W�411Q�,9�^����%  �rq7-��Y�˛,I�=z��B�$�Y�/�������G6�,�KV�ކ�K�ϒ\����&{ɒ��Kz&bFr�%�҉K�\�dU�mh�Ĵ����XN��T�$�Y��,��pn���z���$�Y���2k��%�'.�K��%��[k ��<���6S�R�n�c�m��&r�%���'�B�,e�0,N�J�T��,��d�J̖� K  ���[��֓[�   � K`' Y  �c�,�� d	  ���v�%                    `�n)��������ܱ    �y!�,��5���R#J;��7��$#���%    l6��5gg�VM�s�N�-������,   `�"T�YJor� �    v*tD\(��9{vvC�D'��Yq�Ĭ8g=9���e�A�t0�y�H��8Uչ��o�U��ҍ��,M�4��Jǵ�É�p!3�������^�7�F��7��w���s�Ttm�$��������IHSt�s��VV��>@����d���*:JW|>�%u�X�Q�e�x�\6������̏�Ėf.��    P�J��5��%ڰ��p8��I�T�2���p'B���DHB��Û�,��t��&�%*ENW�o*槱���%m�n*�>|��Sɫ*��I&K^I��d]%�6��5$}�n2�2�7%%�䩶�]�&�� �Kd�JR2�t�srV�#%���#Ct;Ύ����d�.��CD����{�x�y�<yp��׻�4S��    f4U�F��˒��KD���*	o��2YJ��pܖ_��JA�J��D��1�ȩ_�d��=@�(Hm�ʒ4�skkn"G�����m�!��}O])ȼ����qi����L<��C(jK���{��"��z?��G��d��ݯZ�w�W�5�w��---���   �	Z��
ҝw%ʒi�+_���v����U���%�fI��CfWr8�[.x�������RPw%��F�z�2io�FՕ+�cԑVVZ�ɲ��ď�,�T�$[�
Y
���~�$����3�Y   6��J��R�oV�d�J�,K�58�R�g$K�`IDK++s�p
w�²d(Y�� K   ����J�'K�niDI��G1�+vZ�d�M�%�,9h�$7%G!Yb�$U{#Y   �!z��b�������
ٽ��k�ʂ�DK��$�٪�;�,�]q�D�]Rco�+.�})�/Ko��nO2���89�TǷ�]}+�,���ܚ%R����d�@^Y�������   l-�w��і
�-Wʤ� ���FK��,��R&yrC������J�L�T�Ԫm��/K�m@R��'��F�%O\n$ ]�7Yr��o̖huw�p   ��a��?Y2�Q�����o�����gIn���>�Ҥ����mm2�\2�Y��%��X��*�No �F��V@��6K٤3����ii7\��%�d)^~p�    v �5K��RƐ,���)%    ���&˒a+�8Fw�A�    �<�̓%��;_�^ٜo     �B6[��5Kr�                                                                                                                                       �-dϟ�Lf���~�r��qg)�tb��;y?Y[wd$�����W�ꆦO������F��T�7rJ;X��zѓP����O[6�ֽ�݁𓻟�dS����䷑P��t+�   �EٲTQYyf&��������u��>o�$p��/x�W�Z:.y�A�?l�M9�e�Ü)[����   �����g������d K�N^Y��ŗ%�%��T׾��x$���M]�_  (�C�
d	����&K���}w+�-]*"?ē�������  ���!K3�{N�dyMp���U�iHɊԌ�TT�Y?&�I����ʪ�3����~����5gg�����~�ъ���C�؃��%U5�gU3Z���(�,U���x�L�����s�L*����c�s�t(��j��w�O]��~���u�~0��_�lh:�IF�n��Y�nh�˙ʢdFFY�q��uT�`jmm�=oc+=���_-�T�Mm��-�&uqr�v^��<}�|����wN�aR����}�2����|ӽ���ަ,5w�}�6u�wu�O@�   l��2�e��KHӥ={Ti�p]�SQ�=-̩����lVJ�JK�**��
���Yb���bHT��5�2e���ydXI�Wn�c���*g�_Fٖ�+%B�����!U�5|0VϨ����$�kl���+K�)}4�������7]:��ڤ�%J�d���1$z�����X8^��y៧������\�$'KT�TCb��m]sG�RN5��Jv�� K   6�&K�!�d3�$d�sh0�	qY����d�%J���G�h��REU��?�ˡ����
Q��fRL�ұ���d��J��v��2�ٖ� ͪ~t�UNU��ԍ�g�.)����G��W_x3	E�!jG����I����ɜ�������������GT]R�˞��jl���U�eI}�7w@Y��.)���^��I�dK�Y  �Q�:�%�JYfK�,I5K�e�fK3e���R�;��9����2�Q3��8u�X�AY�dv%�5KF[2���-���[
�c� K���(1%�t)Ǖ���6��k�W�=��,QWRD�$���X^���VfW�e�+�J����IbK���;�=��)�q d	  �FEKĕfU9Rm���taY2�,IuK�R�E��]U}z:=;4���9ON��%-�b�[*K�pi��q�����D�>�rY򲿊Tt}X�)@��,ʏ6$K�`IDK�˞��*"K�`IDKKK��=d	  ��A%U��gH%��N��MAY⦔I?��6�,����{���OW��N���
���ydi˓%�dK�鮔_��)YR�~@���O�,�%۔$KJ��d	�  �� +Z�p��NEd�u%yA�$K��)�����3�����)M�7����k��"�e��R��,���P22�ݨ�Y��)��C�Ↄ1���+Y�s���HfY"���<�os}7��<�
���]q�����A뚥@�
oZ��7��}q�5K�
�R�,  �0T���v3["oC�������3YnKZ� �v8���"�Z%���w�]�)U���2B�xy7�@���D�*R�-6í�z��J�J&��g�.�Ys ����ǔ��w�"�����4���zՔ�����kr)'��);�fH�4�1�x��pI�K���X� y3I�F�o^����˻���yw�N K   6�!� ���a�˒�d)�IM�6$K���R�>K-)ܕ�;e�	�'�,e�u7�N��q|�t��� �%y4�TT�W��.K$Q�v����lJ�l��J��R6m��\Gyc�t<��L�ё@Y�G��O�In�$Qi25��qѾJ���y��\�d[�-�tm��,e��E����8vI��ۻzg��In��5�(U�hKʈ��MG�.ں    ���ę]	     8�+��r%     �C���
T	    @F�ugaJ                     �"*H3o�uS,�ΏWVג^K��K��R�Д�o��4u�~&�N�S�%ڡ��LJ�����$  ����;��= nc0S2
�R���Ai�#K.:.0���⟕��%�K��,Yj�z�o.�6YZ_��}�\���<���   �#��sOh6�� [*K̕���R�,myd��;1�O��� Y  �mPY�aG&�^��<���0�����,lۑ	�  �m#�,��p��?�9-�':EWg����p��p�a>�����l&��s��ʉ&���ֲĦꊹ_���<�D�鎈��T|�V1�"�������7�!p�qtz�6?�O�%c�F����2>�ɽ#t�n&X�����Q����K��z3�A�t��z��-���T�7r���q�|4*n��_}K��<�0����c�����l�<�8J����ب/������ctk[:���#v�Oĩ�,�8^�$M���#Ku����_�6u���й�93��ԸՇ�t�2�^rj�w��B6�U>��*�2q�  ����D���stU�y�?�'Y���T�(����!���ѥ��)Iβ񹙄�n�g3�Е��5(U�Ԟ��/Kt�n��έ��;2��%їR��D�j�\��7|RS�p��#��K}��%%�VW? ��A_`�l�yO ���A��N�x��\�՗t1��$&芃D���"ո�?U��k:Iכ��uR���	�KL�tE�on�����/�%��C�"�j��|����qɛ#KT�� ]:T7^�Ǉ閟,�i�^�����������OJ�Tm:�V��%O�T�y@�"�o���UIv'$K  �[),K���w�-��	��[KYbv�UI;�v�d����R(��,�����J�%*�������K!�N�`�$u�&�4k9Q��LJ*�������p:����
���*R �v�D���k�&K��5�Q[
�|#4T
rU�g[��X>����$�� W%q`,Yԫ���7%v�㘪A�H�h����?������8���ZH�����n�Jq�M�  �V,
�C��|Ns%[���J"iJ���e8�*����R�+��q��̦�+�
< ��O;�/K,[�T]�K� Gs�osY��]��Q�yO���z�_�%y�M��J,M�$��J�d���J4i�䉯�}������J4[R�h�����.�6�w�"K9��p4w����.Y��d
�,]Z�OgT%�  �^
�,�&K��-��v�,�58�u��Ȓ�d�߯�,�h����LY�kp7$�Ĭ�T�D�'kpW=CYڼd����>|z��$J�̪Y ���fʒE���#d�"Y�CY�rSJ'Bc_�Se&K�(%Y�ϕ�,�Se�"Y�MY�uKJ<�,,(R��  ��re��ˤԧ���̌�/����%-ͦ�%6�/K���DIxۓ� �ӓ��@ޚ%+Y�ђ'�,\ˉ�xywʪf��w{�8�����%R������^�d��ͮY"�9����1�G����mcS]�K'����[�2]�T��3�w��/�c����g�   �I��Ģ��Y���7�pig�˖��"��ȟ,эqz� � Wl.����K�w�Y�o���h���	h��Xۀd�p��,�7ñhi�7�~�����$�Kܕ��D����9[��ݚ �솣ђz�  �6�v�."K"\�.Ҵ��t˷�Zl�,�,�%+D���p�chy��r��:�Y�K�҉��Y��	���R���R�%v�T������6K�>K�ʥ$�'�Y��T����р��Obh�T�ϒ�fI�K��$���Niy��r)!o�˛,9x�$nL���G�o@6���&�gin��K�U�    +rk�     �d	    � �%    �@�              ����&��
endstream
endobj
19 0 obj
<</Type/XObject/Subtype/Image/Width 754/Height 258/ColorSpace/DeviceRGB/BitsPerComponent 8/Interpolate false/Filter/FlateDecode/Length 17163>>
stream
x���zǕ�� 	�"j�'s��c[�-Ų&�d�'��8�I��8^�q��H@-�h�����1�1]�������EI���t������S�ΗH  ��1�Q��                                  �ǖ���_�V;v�z��G��cG�ʍ����O    �i'�j2��S�v}����uC�c�����ϴ�`5   �S�@:s���t�����{|6=�=Y��ح�W����j    �H���j����iL X    ��`浙J��?q�p_V�ʝ,v�qĕ�0�R��ʽ'�i׿����`ֿ�ⴷ��`n���Vm����|{r��%���#�ސw;��O^��Aft���M������_ج���glmx�޳E�ݥ�{�Z���6�Wq�����7��5�7��_�K�v��Ղ�gpVW�#{|��(/�q�qg��r��������46��Hdw�������o���8����cϺ�ܗ��{��   �'�4�o&2C�i5��@&{d�j����9��n�J�ad�ì(#�ƻ�ӵ�_�6��dGw�O-��dG��,��T�I���1g�f5��[�3o'9�d�\w��+��%�e2c{�{�j������k1��Vmu�/Bi�����}�߸+W����V��+f���X����Dbt����܌��>s�&��Af5�cm|��ԯ٫ji��ק�=�������   x���]�H��j�`üf�9���f5mJh�w��He��p�,�r}c��.?íF(]`�R&�!��K7rmm�*���ֽ�x_�Uf��Hj�\p#{�pShY��(?eҚ�����c���}��ώ�/����K��y�7W�՟��={����r?�   ��5Ը&s��D�V�����|�[ω���<<�Q�j<�9��D"7��L��q�.?CVS��F�;��̰��x{N�1Wj,Y��HfVW�Fvs�Q�f�Q^b"CV#�4=`՚%i5��ʥ?e��X����?��   x�P��_���-��iLN��U��dj�y@V��jd�fu��a�R��j����V  �)Gw����[3kٶU,Z����V��V�IP�FU�4�nVÕFiF�   `���C��u�CC�g,vf��zwv��&����W8�j�,T�Y����a:Un���^���Y�p�U���'��������i5�;8�Wúi�h�ш���Q��°    C�FHMGך.VC-5�-L��3PT�)v?�m��5N�v�SES�X�8���\��ܮ=��h���[�k�rĦ+��9o��Z�(?�ĵ�Z��؁   �v��k5���-������j�q5�Ƌk7��h�kb��6�F�Wc��V�i�8��?�y�b5	}\M��n[P������Q�jZՕ�O�V   �~����4�V����4�    ����V������    �^��Ӆ����G;�     &v�j��l7                                                                                                                                 � yh�r����sl��L��L�C8v�ޗ/E~r(wd�Ҫ^{�a>_W�#�ޘ�ߪ�����Ə�W;�������ܮ=g�M����p�v�d�<󛫥��K���]������hZ�]���x6   O۶�����c�.����'�����f5�����⣵����?(6�K��~� ���������s�  ���D��?��	�b29��8��GN��y�&!�&����=���5^���[k��B�  ��������D�C��Dn�s��j�Z�AWGaJ���v�j���߂�  ��N��O$'����:�+�xJ��:r�&���M�io^�4�������ˡ��4�u:s� ��n�_���ҙ�f*�����f�N�
�v�W��I�N���[M&7r�����s��詢]�\�wC��;�O���}p07zt��(/�]ܔ�u�ت-�SV��[n��Eat�Ɍ���y�������c{���r���3�k�������9��M�r�x>����{��M�[�Ռ�{�wϰ!���s?5��j�w��w�,h  <�-(k�vM��O�k�I�n�5�TjbQ*N*50Y�(���j5���W�+v��w���j�Ѹ*s������l�j2�#3��X���Ū�f�9k�Zå�Y����S�����Uw�U���Inl��b�ոJsl�����g��[k�M��z�Q�aF�T������B�U]������~�`�7�����2We�Rv��s�ִ�C������Y� ���j\��w�EV�I��8a5���5�F�kL�;P�_�d5����)������ �K�Oy�����۳V�)��J����0�)�"�����ŔIb�g��X�����ռ�Xr��g-�1孵��&��}q ������B����?�W\��+��]�kl�3��iT�q_��Ւ���E��X���s��l�7�l�mA5+����>o  �8����Ր�t�֨V���D[Uk�۶^�io^|�6��I�oߥ��V�Fj��If����e5A���W�kM@j,oω�iM�\^xV�,��3�Q�kBR�H��u?�v��^�`��Kj�5WkJ++���*(5�ռäƒ��ȴ���|Q�gm��m��&��@j  ��G6�0��O��jY�bw���j��F��²X31��\��S����صFk1X��Śz}��Zo�)p�aR��ݧD�T#�5��݇n5K�_E{k}�?�M�O�����T#�5++���a5Z�Fk����m[W�
 �S+ѸV3�gm����o�Z�PǾ!��V#��KS��zecq2}|��~m��؜����^�I(Z�/5�V�j5��K�3�ab#j3�ZMl�����՘��k5�(Ե�4  ��k��r��r���$�Q��V��l�����=���L�U�EzSn|󾹯�\&h5$5�VC�V�+!1����b�3P�5S�oN��I�Ik��4]�	Z��%�w��Y���;8��*�V��E�h�)uo�^�z䉝�ju�)څ�@���  ��Y�e�>a�5�me�[�&���w��xǹ���SQ=��4���ŗ�w����@9�kD�0?�M��C	�aw���G��}��if,�Z�9���k����[���"z�y������͵fh�U�����@����(��S��8��AX����3P-�5�W���n���̳�y�TSz��Vw��}4
Ci  �i� ?�]����}w���j��8��j��蚮�j�Xc	�����MQ����8ʖ���3�������2�5Ji�O��V�����ǜ�ǵF��:��c녛ѣb���(}}|��l��ը1P�Óݨ�j������(ͧq��n��`wMl��F��~�������H�.���h&�={.�o�q5���~�f� �	boݾ~6��   ��8	�    ������R    �XB�	vӂ�    �1E6	w�4                    @���n%��iFt���cP4�ϛ�R.������Q���C}��������rmu�/�?����y���䙦u��v�����[WC_X��ś;��   ~��j�XW[O��KO�ՌR�S�p���?���Ϲ�c�7������pñ��}uf��  �#C�e� �@Jx`��-~��S�Gb5�Tam0M��0s�a�w(�+M��*  <A�((?3�Ug&Yb�ii���$�Ĳ~�]�Q�yĵ��g~��n-���)ͭ/�ڙ/  ���&o,��'Q�\֓Ev�اv����7ڥ�P��@����d$TO�TK�K&[RT�y��kY���@%�����_��|e&;�:yj��5�`��x��()P�T��(��d���;T�aiO���퍍Y/���{d��L�d�9P��=2����a�N�jd\�'8#{����\�QP����?����`L��Ʀb8�����_G�Ռ���-��Ӯ?uw��٣^8���Z�:l�a��Z�~�����?���^�xrE�ͫ��F���o�������n��}}�?���m�C�����uͿ�T����%  xP�Γ�iLP��b5���o�'��}�=e�{�e�ZN^�"��-c�����N~K^�[ڭ���y�v��^�7<ϒ�v�Z��p����k�o&��M\U{h؀�b5����eEp(�;h5�f4��dGG'�{M�jx�Ƴ�%�2�3o��n��v�cn4��h	�T�������Tj5ݭ���j9�g����"�k����5�֘�fl�s�n�4����~�re���,5�֭���oΒz��=�����_�1�4]�4�^x��z��p�i�u�y�՛uX  <:�Tj$!�	i�"5��po�b��qH����Z�5�t浙���-�V#�F\82SaZ㿒�e^S!���'�4&�V#�e�����ѹr�򌆹Vc57���[��vs{)��]�*eExX���9Ml����RdPw��>k5t��ڸq&P�!��Z�!�'�lӬܾ�m%�jh���Z��T�YW�yC(���{��  �#�7	s�I&y�m(}5a�a����K��&5�v�ڼ��sQ������''$6d5_jx��`��]
J���>YhWW��!5;f5ےc_�l�!�u퉹�h{NRx�	HML���Mjv��ƕ��͖�4�iS��\����s5&5�f����?�mv�������y��$`5  ��	�jHnzY��5�S��N*50Y0���������V�7qzZ�/=tػO�1Z���dx@f5l��Ю�u��)�a�O�=���@���]�F+�H�Y[[۞��W��Gǫw�j���RTG͒�~�W^8���~���1Z�~Z
t����۲�fI]��j  �Qg5��\>�H��VWi^�������B�Z��.6}�j��x�j5�Z�V�x�j��j��S3X��bYM���D��/��o�~۰�  9!��i5�\3e9�_�RCŚ�y�{!5Jwp�V�b��lBVå���_���z���WC��1�=il�jZ#�L��$f�޴0~�|�I�M��Ռ�^�V���Y�Ru��L�}�����܇�5|��W�s*�����5d5��{�N�O�w��k&6�4�!�)�VN�g�  x���o\M\��Zc�:�$��&���5ڡ'�*gj0���.��d��X�Ie�#P�.\�g�ª5U�߅�y�{�~��Wk��y�m��R֢�F�����F�{=g9ժP��������Liؖ�8E��U�߅��@Q��~�ۣ�3P�=��n�ұCüZS��^���Zm��N�x�����7�c���p�}ad����ޜ���}�d�����C��G�����թ�|  `{h�����j�F�<7�r/)RCP��zS�#P�\#�c��8�V�Jg���k�;��=�^�I�kT�Q��x�j�q5J3�o7F�Q���w)v����ּu-�j����'8ZMk����./4T������}���,{�j�q5|^��{����W�*6���ê���j:Lo�r=�<y�Бܾ�� G��zC�P������P������Ռ���^���j3��O޺�����5   v�p_xB �iZ�]nHm�����[,�3�  � ��<�Ёn6�&ԭ�M�����U�P�   ~�j�Tv����bG��S����B   `g��                               ���Ӆ+Z"�d>8׾�\e��u?��g&�VI
|�G�n^�f�ݶ�	�22j���Z�@�������n�6^X�-�3��h�v��ɍ����`aq��cm�|��)���!��]o�wU�|"�
�v���    ���!�	�?%���8���dA�KRM��	�^^JS�)�I,�,�-+�d�T��@:s���7<Λ��'6>b��)M�)L�b��ؐҔ�䤳��Rb�r��R^�aP	���*�'6��d7�<GAZ���EȎ��Yj�7y~�L��1JB��    ����n^��e5T���x�e0�_*�"���z��D��\kHj�D�T:�H��Q"����XƠܑY+��PT��̟2F\�G�@(�iy׫�P��գ`Ü�ت~'�3�����]~��#3:~l�l   �i&�Մ��k:N�}#����T#j2�Z�C��4����VC{OeY�!Hk�]�5��T��qi�]
��   0a5jS���~Bn?��-N~r2�n�_J[P��n�gr����X"��n��/D�?q����ڂ�[5èaڂR#�#N�2�3�VCNc��P�FkJ˟F�N�V#�5w>�>HNca
   �}9y�]g�����aO�\��Vc��� �՘�����K�l��E+ƤHf:�%r��Qj�i:���5����Ʉ��d�*{�+�:CZ�x^CNS�8ݭ���8�אӰ��Ո����   x��a5�k��"����Ⱦ���p���@yK��d�}�J����FC�P�0��X��{p�qL�O\i�
�Nc��]���,v����=v��zi��q
��   ��VC}6��	q�[;������q�۱ۡ2�8�m*��~m�{L���c��/�����(Z#Nwۆ�ˁL��l5^�&�4ݭFxM{K�x�`�����wK��M��b	Z   h��Oj��u*�Ҵ���f �4	Y�	����z���#�V�Uih`M<�QNs��T*��G[���V��R�Fi.�|��%���   �t��V#[�yC��:����4��TdG����Tch����ra��D�Z�Qzk$l+j)8�OHM'Rkd���N�ۅ��   b���S�r-䐺$N@I� >�&Gո�s�`����%�MZjn^�4A���ń�*,.��^�Q��{O��&�Sv�ޗ顜i�]]�"�ߙf5�Y�S���V�
�C;��V�������                                                   ����1�&&P�Sp:���gk��"4��g��+^Pwx�os�Q�[j�ݑ���-��.<h-�g+h�/�ېe7+W�!�)��0]؃ؐ�іjb7�>-0A/���   �	�55́�q��+�d(���Gˁ��?*5��6�M �I`K/� �˶+����V������P&�	���r
v�ޗ�����j��n� ���o�bÜ��V߁�ٱ�~S�ْ��L&GK   @0�w��)�2�j�"�Y��IM^-��Z%2ВK�|�U^�����T!u�	�-/�I�[*iPhiiR3�����Z��'�g5,��Z\��e/ߒ�ʍF���b�VË3ec�%�[Z�   @'�Ո�no/*�iM��{�R�(�j5)*�3����o$�5�p���.�V͏�f��:M��Dv�>�&$5b3�.��p�����.X   ����-E�v�j5�Ք.�='�j���T
5*=�&5��eڀ
�jd���vA��5��z��J7�iޡm��V���Ȧ�~*��'Y�i�O�*��w���=1��!����ڂj�   x�	[���<�s�m5�kdw0��0j�m���D�p�P���.3��+��&��4 �V.Ԉ2��V��;iX���=�F����5d5�PӪ�e��~�&=���	��r��U   �饇���*���+�T�'����l���XU�I�؁�څ�[Y>i�gN7�x���j����Y���՚����oJZ��4�Y�BNm֯�   `"��$��O��}Á�����oGj1���xR�w�Kj��(�ly���Y��Zo�a�P9�F#7�r��ȫN�m��ST�&=2~l��2   `�����V��Cޝ�(�i����х��}Z[ɫ�s��0ȆQ�V�~Ҁ'5��<EG�̿U*����s��Q��[��V#�@i   �(�[�h�	;M�c�T'4��;�-
5����zX|�Ci=6D�Pc`[�o@���F����Z��0�j��t�h��0P    1TXǩL�&sH]�'����b����*,>`{]5�P�>�&�vc���)L��*W�+AӡBM���Ķ����/g��S(c�i��g��bXi�(S�F��装y7M��Vs�ο�??                                                    �'m�������;�+rF���M���D`����v'�!¡0(�����	��(���E&PZB`Rq�3��s�OL��FN���3<�R�-e�0w{s��[fGǽ)¡�n�n��n   @�)�%L&����bÔ�5���-;N��+�/Г��Zj���jSf��50�V��Yfeە����t�D��oxķ|��F:M�j
j�e�4����&�MK�JH$���=�ѣsU�Q&�Ɏ�:�ClxdB��I)
����AY-w�̼�   ��θ���c�!2��-��2�4m/J�?Q��N���L8ݒ�ƕ��?U�ԧ���a�B;��`l����VZ���x��4���$�Y�iZ���
�>����n^�)���y�2�2�t��"����1X   Ѝ��V�ѤFlF9�v�u���kIZS��~�l5~�Ff�ZM�;M��	��j2Y�4�k1�-��S�]���p=&�jBRCŚN�]*�G�THjD�e{cc��MX   ���,NV��c�x?� ������b�I���ǏZ�r�V#�5��Kޗ��Fxu�\|y ���Jg���`�j�^���9�s�w�fv�JM3��q\��쫑M5��T�O�]#�t�TZ��)�~*��'���?s���q���   �h�1H�l��&�L�}��}J(V���ӴZ��ώ�5)�8��j�lH&��'�dt����d�T��K7��ɂ�M&�Ո&a���L������U���A�j�Ѱ�'V��i5�����T���    1Jc�}J�����ۅ��JZ�|���L�%��6��a(^��=��Ո�EZ#�F�M�c5z�0�B���y��5V{���~u�ۇ�k5T����`5   @lx?��LC��g��Ȼ�v�C$8y��O�:]i����⧠���!������Ҵ�yI�e5T�)ڭڍ��ĶC�p��$��G��&��ny�~�څ{�հ6�	�����   zs_J�P���3P�o��OZ��`5�P:�z�S8Q������R��h��Z�v�����#���S	��R�zkz����N�Q���(�y`5   @�H�I�S�.,zk��aq�	;��c���D�����h�5	�X��m5�!|���Q���א�X�m5�>j�������z�[HMG�ڄ�������4�   ��D�P�p*S	�M\��W�Na~M-���[��Q�\a��F]��j����-�X�-��0b[MB��_�i�p��R�
�2����S���� >y��4T��K�e67�����                                                    x���	?��0\رo��ߗL�&��_�����8��Kt�>DXD&P̥�.1[80]84Z��(�o����iI	�U�X��)�;�x~
J��X[+<�i��[���G!�;��/J���\a�&    �4�0�d���ؐ�8�+w���rB��:<	ʵ�Wx��
�]&���LK=�[$vK�I�3��b(*=�eq�2(��-�ؐҔ��Ąb�	�[�K^�%��-]�a�O�x�x� �zi�˃2X�pX   I��6\k���;�^�1ϺT��^r(��H��%��4���
y��2 ������3�<S1\��Z��&�jHj��LBn�Ͳ)�;���Ӌ,�R�\��&=2~l�\��Ϝ)�j    3����<��|��7�h�݁R�(�j5�:���Ԉ�&�^�::�;X��Ś��	����X��iIŚ���ȇ6[��t�fcvbl7�   ��oA9����W�8����T�q��z ��/��%Y�!���4������B�~���'���?q�P�o��w~��t���vLN#���V��9��#�W�4�$2LcD7��⥛`_M��l&����2�x�`5   @��FHMp�Дա�j:J�0���(Դ�k�7�l���ޓ^�Q�F�b�MT���K�j��@���x�͆w�����i:1�Fg0˚���x���;^�F�kx��\�iՖ?5t����`5d2�%f2�   ��P�T���0�9HV�u�0��;��e�ӲP��7ڄ�����P�Ы3�>�j5z�0ߓ��]�FC�P�0T�XÕ&�� �5��^�!�����F�E�5Vl�	[�t�O~潃�    :���\���}6���p�p�j�1�����䇾�+ZG��G��i�^���Vs�<&�WSt�ڽ/�grG\��L#��4Wߥ�M���i��~�+;���Rg���FH�   �[i�y?�-,�:�c�]
5�3P��l~+�
5D�3P�n���aZ���4�3PU�V���}�Q����	������B��P����m�¢��4w������9   �'�8J#�jD}F�s�	9L���м�2.���h^���Auۉǒ^CN#�)�O�%T��5��4��<C�¤5����}9�]3�c�j��t�Zy�[�Z   �1�L���)�V�3��	(��'���4>)9�a����>���]b����\l�{�=���i�o�ɢ��N�ܮ�~��oi0;�Kx�v*��
�/����(��a��T�C��O�ڸ�~3�                                                    �^�3����<�ɛ�K�	�ν��r��a!��g	� �N'�e\�����|���3����1cXO�V�ڝɍxS��Ȅ�d���������*-���Ĉa'����';�,   �0����$������Hҳ�����/20�2}<pi�����]��lvW ���%��n.2BlB�a���jDХ��Jg�Oc�M�����Bv+a�*,޲ت-jv�@�K�g�(�4�%���]Bl    3I���aN�Ci�cJb7S�<SCl79MŠ4l�o�*������j\�9<Si��'O���Z�����ʺ$���P� K�.{Y�*�d���������w���+�2�?6oAk    ���ΓS�r��=��/*VC;O,�2�%����Ԉ]'�^�������jb(�LHj�X�����.F��Th׿��T�ш����]��	���j   ��÷��ŉ��O*4N�JHIE�eQ������n%����~���'���?q�P����j���iޡm(a2��Tiվ�(�P-�Z]��{��f��)�gk%�8�4�i��{jTzZmA���o��J   �)A���o��v��$��CӢ��	�ih=h5�I�o�a�N���D[�x�m<1��H��:�t�M�)�3�Q6�X���Ո&a���:�}�!��zMĆ�'�9�W�&��j�i:�    ���U��k]5�5�]��3�.,>l��Q���in^��l5T�����V#���Fu��Pu�k�i5z�0�B���y��v�mjݭ�+Z�  ���F�i�K��F��Z�՟��3��}�څY_M��]�q\u�j�n�U�yզk_��W8�j�״���ZCG���
5�.V�?6_E�   V���[8�<�<�&��ı�p�p�{NxbM�3P|�:iè�j�;�̎��zN�p&*h5�Ps�P��cQ��4Jsa�1[�X�   B����j��$�9�p���g���5)��/�1�Fz�4�����'ӊ^��j,[l?�(�׹nQ���א�X�~a�a��ֈBM��l#��c���@i   �h&򆚆S��E>�O^���Na>���gC�C�t�6�6Y�I��}���EZ&�	t�����h��$� >�+������ɻ�2NUy���
5��1�j�P��_�ƝOx7Mh��q��q�                                                     �N)s}ef7���td^B2��TG�9����Z����x�@V�Ay	lگ��-�.�_�'�h���1@x �=��v���	/�R����Pfwh��{ke�rnԼT�����B�B;Nȥ6^�1e&ȩ���   <��X�d�I�Ob��-���6Ţ-!��N�Z���+�ǃ	P,3aƲْ�Ŕf�"�-�^�b#�ƷR��L�f�	��o�ܶ�8�0�&�,�Lx&Y02+�g����m�-��a�!,�IH����[5]{�:u���f���A��	n�֮��7b�u	�'�z���M	��A��-4&�PJ����&�R%	Zl������P�   ��BsҚʝ�Rd�[�,kom��ը��\	z-W��V�2�vK�~�z-�4moow�Y��.�TZ�n��%f�[r�e_ʠ�iz�(Mg��nbm���g}h   #�=��a͜�nk5�4����Uk5����nfy�����T��VHk��l0�o�!���~K���nZy����M8Щ�   xx	*�ߔg��Q�^��v�rmw�4_�2��Z-6y���4��VCKP����g�7�z��˘f����o*�#U��Iͨ}Ǥj�������̅֙������   �o$V���/��\�3���������$&C�s�V��T+5��̶r�)IM�Z����5խ��Ƅ�m��u�;�ˉMk��i�\�i�   �s�(��J�3�fd3Tlʋ��Ӝ�լ6�T&خ>�3�jXi���LgLDx�i�.V���j����I���*�U(͕�[���+��   @ �i�1��T��~�{�[y�r�����^�:;����vL#S(·�s�jdww6�빎˞�lrj��<�����-ޕ5�hVx	���ݱYL�ҕ���   �sN�4&bS�5ͲW���j����G�(&����e��(��������0�+"J�x�=P���W�(��p��e�9���0P��<��1Js�4�4�l   8�ĔF�?�S~�언���[8�Y��4_��k���J#�hC/?���ھ�5��Դ�������jDj���8JS>�J   �f�w��n͋
�eNոIa>g/r��³}�p���'��[���I���o�˳N�_����z-ħ?��Q54�d�~(54��R��6>5g�f5��	~�����i��㣻�                                                     �>pg��tv�tU�a�8}��������TᎹ;y)e
���^gB}����y�ҙ0�has�p��~ü-h�ބ<��'�o�}Z������j���m��rk��]���e�G������4��+��n   @PJ���FK-6��-=P���Z�V�u���-;�Jz���e�����Q��FS=�����qbLFݙF��	���?45��3�~6�=�)�([������ȧ�D:��.�D&�E�PFl�z�wB�$LG����C�EO!6   @���(�!�)Uv�����r�\:��x����Pi�iR�tY�Yro��[�5�UH��Ϭ�܆6�����R�����4�t����n���;h�N��TB����l�o���FK��ƕ��z�   B���F
����u�.��u�����I_}Y�S�e�vIkO�]���	Ok<f[ͪ�ǐ�$z4�w�֔.�����S��Z��$�i�Y[M˝ΔF52���   �%�|��j���v˳c5�G<���[&U3���`V��5㓇�_�.N��fPS3KQN�F�5�?m���q�.UB5��Fk�߾�^HN�7ɚr�fa��L��fPCpk7/:a�	   ���jHj$Vc�F�Å�<�X��v���z�^���0�i��xM]�Á�p�&"5���(���F�W%8��j��\���� OGo�n(V��!������,�&�q��O�������ˁ��iy��͆,	kO   @�(����f��߽eV�Xl��<y|�V�6)8�j�k�	�����$���+P�4���?�Xl��%�=�^�U����PkDl�>�qw�vtʏ�4���+kM0��i�!��L� ��    ���1M�%�q��'��Ei�kaVص^hr����i�AM^��w/��Z�uq���n��K�פ��4�K�9��jxSw9Ws�����.��  ��/��FK��6����� -L�S~JXPRӶS_��4�AM%5��,��w��vlgwm�ՄRCӛ���<-����R����Az|��̯   ��TP���	�4tX�s����ƈ��0��dl>��U�&�4fP3z�I�26���c5K:V���4���ek������i�52�9�:�O��   ��f�&g��l��BI�s��=������=s[�Ò���Q���H��L6z���5����5&��i��˳�?�/n}�ܪh4��S��=I�/q"5���c�c;�f�jhP3�Fa���uH�                                                    �9�t����M���y�Ȼ�v;�OuZ��n�>bح��74�A���n�M��~�[ܭ�n��vt�����������ۿ������9_8,L઄i���/�W+�泅�{��n�{�0�   �++�8ZlXh���-��c5R� ]��*(����,4y�<��r(S֭n$�d�?�,6�i<��7�n�2���[YM'^�ĕ	�)��-+��څK��q���
�'����qw�v�k5�/�9�F=)��v˅b��f��k-[����-�v    Ɗ��K��V*#rc���4y�{�s���F��-۪�R�Ɵ�x�l4�����JҴ���1VCEPI�4�yV��4�ld�P�e2�J9M'�n�3T�ԧ��2�}�2"7�Ր�LNm{7�>��:�y���Ek�IJ   ,Ʊ{�d5���f�����V;X�*}��V#N3z�������SX�M̴�@jhX3�f��g�bZ{J��F.
��5�q����T[���ر��t���   �9͌d��^~��'=��۷n�ӴǓ���e;�����8����l��q�/j���Ȥ��7&;����ѡZ~Jt�F�4���Ng0x3�&���aM�۷�E�Ոר4ͯ��c���S ehx�I&5���&U��n   ��dF����4��V#���V���Ƭ@qjX��Vñ+5�)LFn\���������P�O���\3V�,<�q�|��XMn���FE�Y��͆��˭=)Z*,1		�P]��    Jqa}1f54��sYkr��
��䓓����X+�v�&b5~P�פ��|���~�5?&��錉W������7E��E+P�hh�q���̰��q��v�6Z�ݭ��   �9���Ӛh����x��ס�t?�
/a5��q�4%���V�*Yo�V�P����xh��<������2�{w`5�����9�'������v%&���    ��`5��@ia��DN�)[M}��4�n��p��W��7�{���|�n{��Դ�IM�jhP�{�i��̻����zKSFiN��������ƕ�ϰ'
   ���=Pv����@����հ�h��������|���pg52��k�!��ό՘C��j/?��l)���j�c�f큚�Ϋq�5"5S_k�)�p̆(
Ґ���   ')<�#5r��O���M>�O.����He���r�>T���㓇��)���>��o55%6JeL�E�iXd�P=���u��YAi�s������p����~���F��r)U��p�&�����=z�'Wq                                                    �C��;<�6�U��j���I�[���v�ϤBKs5�u	Ԏ`�:	�e�֭ݵzc͹�,\�BKs�T� G�bk��9[87��Up�������.����.�La��&��ns�9[x��/   �A�ݒ/��8��.�	J:-u�$�ߘ(i��.	�L���
�խ��q�[��1���@���
����MzOvT9�c5��k��@qiB6�{��t���ݽ�~T��[��	M2��}M�O�jT�塭I��    �[RS���<{�Ux�)����MN��J���Ngj�F�_O�l���u)���5s:����}�2"7�j����r�$�4Tv��TfF�e��ݳ�QZW��~�wU�Ʊtv   �AM���ܛa5ne�3�����O&/i�T�-�F5r!��ˬհ�L���bT>�d?�d5�����n���&Y0�Q+O�t�{���#��@j��{�v���|�!n5�n�%if5   @�كv���;��'��[�e����d��I=�I����-��Mi��t8���9��$��[�4i{{�3�i^�xV��5�7�����I͸}ۤjT��w�����SOV���Q�Ν�n���ﲄV#^#i�?   qb���o<��*|�3�q����ѐ���Ƭ@��X��f㇈=
w�VoQ*c��.<��̵������9�
�ε		�P�Zv:(��l��Gj�I�k��jl6�kO   @ȜAݦ�p�OkVV�vPS�3vʵ?(�O㓇Fq��P��?�5�͵��ԏ
�tƄk*XMM�ƌ\T�x�
Y�V^�I�߾5WfXMg�:��Z�ej�   ��KԘ�^�i���m5
�بYKj�0��'�ɫ0+���G�U��L�����yw����1�Om��j"�]P�i�HVx���=�z}Ņ�5WÛ�˹��|||t��   ����l5++����*H��s�?o򠦼���F/��(��������2�Yl5Jj�wvi�F�P�$<�f�=Pta0MGݧᶨ�j�a�=P���xo��   �_��;)"
endstream
endobj
20 0 obj
<</Type/XObject/Subtype/Image/Width 791/Height 293/ColorSpace/DeviceRGB/BitsPerComponent 8/Interpolate false/Filter/FlateDecode/Length 22447>>
stream
x��wSW����p�\�B�$�����s&C� 	�$̐)I��I3`��H�nز�Ʋ�0��V���҇z�j{�]$m���p_�D�I����Ž��<                                                                                      `=��5�?���y���BCK����B.�2x�y���:v����B�8��@��Qnj�ܹ���������>_    �$��ұ��t:��=�*|�3�Kv��m�si   THM]��A�PP�+��~�_Ƴ�%j�R��C)�p���T�y�(   �B�?�����?����Z$*�C�   TDm}��������K���z��gJ�<�;��	�z�lb����C�('�K/�د���!�\'�z���7mhl>�ߌ�c9��kl92I<�{��{0�M,\K��M�G���Z��C���ko�ީ������j��y��2���?�WZ;�|/��s���4����\oh���^8:s�Hׅ~):�-�"�vi$�X�?�ߦ�c�fM����h$^��ׄ�ry�r�(����V'{�1U�j���W��剋p,   �L�b�$�D�I{:��&���R��Q�T����C��_��O�RigC£�|�\)�T�K��DI�����s��sӹtd�_��9�:�hu�p����0=k�B��[�:.�lE�J�S�_��\ry��(j^���͖���Le�9��i=U�D�v�읱�W!_�|��k�fJ�%�mǏ.�f��[��Jөc   X�B��j��M�1Q��%c셜J��q�2AS)&N$���r�J$JMGG��Nq
�ȉZS�+���Dx��>H%�������I�������y?yQ�b�D!�F�$��WW�u�(A�弊$��P�P�Ğc�Hl��?+�J   ��M�S(6����5�L��K7lӟ,U�DE�2$�ա�k-�Zx��탡Y�#+{Ӆ�(D�V�$Q�䲾_�"QQáhu1�^��v�K�͡<�����Ss+�J   ���:I]�s(��e*�2��]��%ky_#~t��EQ�-���lh�i�ڻ�DWW����^��ky�ߡ
�   L<�$ʸFJ��G�mh%��K�G޻�h��n���`(�:��O��H�C    ;E%���{hP!���/��E%�FQSjZ/���H�@�{�t�:@��c%��U�ِ��y��������z^*2t��ѵw[��Mj�VHq��&Q��<�&��Ej&oH�׿��H�I��n���:�D�(��A!9   P�b��`���Ų���PI�o�#%���<ysM��|<��$�-�� �F�Z�B�5:���k6�rb-%m���5k�Ԡh]�h5��4�ZG���2�    D�r[���-~G�I�l��2%Qj&>qFZ�3�D�����lp-E[̕QL�讼x^4�j�E��K}��&ʨ�b�TF����K��Q�&S#g�HO�iÙh�7�ZC�(�M��gLdJ�'����Z���<    <{�5Q     �,�(    �*�D    T$
                    ��,J��b@�E�������w�����Vܵ�:;IkM�)j~��|�&�e�k���(���s����?����&&�ϧVǿ��~������OG.~���	  ���F��M-gC����,�+��G���%��(ҵ<$u)7���*�<����%%�e1����w6�z�$j�O��\t���Y��  [s�r�#�7�� Q�PR�6�P�y�p�e�O>��������U�$
  �bP���m*N��3S�ѣ Q�*Q�Pe���Cm) Q  ���wCl���wh0�y�w��g����ӛ��527oJ;�{�I��s�G�JDFSO���2�����Y'ֱ����<;/����yo� �o�w�3ʼfL-~�༂��'��S2t���'M�3�!*yh���Ν��-��Ż���֮]��|*�d�4�Dq��g穩�	>RϿc��i���G{/�˙����S��v��dT/(J>}p�����{^�vN<�x2v�Mr�y羿����:���]�}S<ռ���%�S���7������߉�L�'�~BN�<�D���K��,Qr��Jb��Y���W~zm�Vj���2�}�?���cK�7?���G���2���oɵ������vt�_^g�
���KG���^�Or�پ����7~���D����'�W��>��~��\l�Η��O����Lb�ޅ�����_I����h���.�� �L%E���3���a5��_ӿM�:�z)�����_<l�("Ky>�����lH5W�D�a��l�0=li==&&O�[�g���������N�N�����9jPY��f���L��A\&�j��qq�*QL�uj���K_��+Y}�pk�Ξ��ն}�i��@��o}�JF�ص�X ����ԩq��c�Jrn�B�O�x�w�=;$��}��+sn<���k����p���QD��$�#S����t��5rc���~b4��tJ�=�k�O4���I�w_���7���$j��7��;����Q�_���Y�D1�J��su����WJk��	*\�/����/�?J.���ܒ�:������2��5�\l��S�+??1�L>��Jl��WT��$��D��GL������_#�  3ud=O3��_���I7(~��`�Z����^���_#��G�ǋI��Q�5���a=�\��Z�܋�e��rM�â*��2-�+�(o���G"�A�k�}�;�j��CU�S�I9GlJ?��X@I�M\dE�����ZTdn�f�JS)��E5�������PL��A��^��v�&N4�
s����F���k�����5Y�J���r��D��}��+�՚3��E���J-�J�L�k���_�������^J	s
�}���_}?�+�k��F�-k� �  ��zRUޡ�D���x��7�Tj􋢏����Pk�(�D
9g�rYE���Z$J��e�=�b�*�P<�"�{{��DQ�RD%�i���-&Q��J@����Q_�K�<�JT�p(�E�$���V�b����¡�M��r(&Q��C�,jV���I����i#��J?��R 0lq(�Uơ Q  �S[ߠ���� Q�F��"V%(*Q��(��$���(�d*j,�U!Qd-���\��ױ�h@|֚j��A�����&��(SI�!rUE�(��I��r��[d-Ͼ���b6�8�Sb��zIY˛U��VI��j�2Q"�
檓([u�H  Px�!e�H���L���,Q̠r�ա���ړ(��f2�O��I��)�U�DU�D1��4��.�(	^�=��$�x�7�r�($Q  �,�*����j뽇�~e�(�%���g#Qu���E3��W�3ZK��.�h*lZ���}z,�����p4�2x��C�H�G�H%����ݥ��9�L9�D�����=�e�T5QZY^�D�K�*�(�?��=�D1�Z�}����W�w�e�鍩��e�jj�d�bE렊I��E1�z�=�^�v�}zλ�h)y��O�u��E���M�,�/"Y  ��#�WN׹CLe��z�Oߜ�l$�EQ�
�(_s����u(EJ�h5��dQl;�fQD�D_��<�_�9�r�(�����HI��f�Ų(��y4�����YĤ��k��!�ƣ�T�Dyx{���(�;O�]�J��w��2+����^��<�op������D�6��i�0�dQ�j\_�+�;OP�D�,*�Kznw�%o�+.Q��ARh�ؐG����y$�Sr�$�*jTIfQ�� ��Hs��G��d.:}�/�v��(j!�,
 ���+�l�#��[�E�(�p��UJ��6Qƣ��AY��a�޿�E�(�"ʩ���2J�K�r���S��a��F���&J���2%WD9��ZF1����>�u��K�Pr�(�Oٟ0>�}�y�>Qr��oo@��&J.��\r켻$J�������ēQ9z�TF���<��&Jov ��2�5�xXȔ�D����OI�Pr�(�}�Ho(o�+!Qs��oo ���w�"	T�fNAM�0��}J.�:�˓���P$�m��fF��Q�  n��D���k�^�5Q   ^ Q`3 �  ��D�� $
  ��6�(                    �)����L|�?���:�vQ�����uyC����,dO�ʶ'_h�(ќH�����I���R�W�j��B����S�y   �R�D�mv�E����j$��켍�(fP�v�/#%$�e1��S�rH  �lX[��ٕ[o?�/ec+HT5�@�aP�RR+{�|��f�v,W�d��.�Z����I�s�_��Ӷ�g�$&�֬<iϣ�^��d ���+  ���fT�У Qϖ�c_��ҳ���PAE�}0�$Y��U��/|�yv�f[�(  � j���1y��>Q��Ӿ������1=��ΛҎ�l��4+��Iz��m �`4�������:�40O���<bJm���Gl�'�!��g��'��YĶ�؀<yx^�<�����0�?A����oȄ�/��S��yx�4;��i�ڥ_Ȼ�>�)%Q��<�O���y�����^��Mғ��>,���>OeӇ=�OT`��譣��ڵ�1=�!O-zޔ�R�'f癆穮�UR�e 1E��bv�:���;�~v\��b�9�v_lu���(�������� $
  6�J$��%����b����m�ԩ��xxH�ŗn�7���N�$��G����LL$�"��5ke�����#ůI�[�g��������K��$QM�N��Y��Ac����gD����ITKǎ��V�be�Skgg�]���\1��v��.�Qm�w�%���֧L����CjN�]��|1@,�S��=�F���ą�����{vHxS��}W��x5(c�pǞ}g�F��Ӭ�f�^#7i�M:}X4��tJ�=�k�O4���I�w_����]?~�I���{���/�\����^��J���8W����}��Fq���bM�E�����{ǯ���}}��_]�>��c}��r  `���i
��X�c�-˵�cԢ�D���ҍ����X<>�?^L�Ԍ"��X���a�U��z�^Tw(+��h�U�D5�u~4��J��m���HD3({���}�Q�p�JpJ�4i"�M�g�(����L�H2u�QQ����ݬ�Si*��������6�J�IT�hY޼���\'B��B�KD����O��Iٚ,X%JPz9�A�Z���كՕ�k�u�"/q}V��*#Q}7��K͢4�����+�(  x�0w�K@eS(�}�[�K<���R��G�����Pk�(�D
9g�rYE���Z$J��e�=�b�*�P<�"�{{��DQ�RD%�i���-&Q��J@����Q_�K�<�>��dQ3�`�աX�D.��p�u��up(�E9�'�R��� ��"�xcJru.@_C�  `��sWY�$���(QZ�j�E%�TŞ\�Dyx��LE�ż*$���3��T��:v��ZSM�=�Q���D�e*���.��Qzu�\�,Q��Z�}�M%�ljq������(��7�<:e��*q�Ye~��w���%�ǈSK�t��3��ˊ����>  @�P�*gQ[D��/�d�x��&g�b�K��d'֞D�?6��|���M�$�L���J$��$����?���p�DI�*(�Q%Q�{l�$��6��,��DI@�  `C�ITm��Рb^�I�ؒws������������ȿ����%Rt�^46-�Q�R�>=aA�jhi�p8�\<��!e$�#J�K�|i���ӎ��K�j�ZX�xY���D�����,�F��%P�K�G���ҞM��C-ξI���+�;в����DѲ�Teeɡ�)�E��].&Q$~_�D ��n�S̾��\-e��z�Oߜ�l$�EQ�
�(_s����u(EJ�h5��dQl;�fQD�D_��<�_�9�r�(�����HI��f�Ų(��y4�����YĤ��k��!�ƣ�T�Dyx{���(�;O�]�J��w��2+����^��<�op������D�6��i�0�dQ�j\_�+�;OP�D�,*�Kzew�98������$ʳ��_}�� �g�\TN�FlyE�(�p��UJ��6Qƣ��AY��a�޿�E�(�"ʩ���2J�K�r���S��a��F���&J���2%WD9��ZF1����>�u��K�Pr�(�Oٟ0>�}�y�>Qr��oo@��&J.��\r켻$J��������ēQ9z�TF���<��&Jov ��2�5�xXȔ�D����OI�Pr���}��Y�eH  l}�5Q l<��(   `���H  �-$
l Q   ��(��D                   �Mo�f��)w�X;�    lu�JTCc3id.5�t����\(���ބD   `���o83UpjZn�z��h�s_�   ���P�
$J]��(    l5��X.<sfjME'��Yz7�,=_9�/�����tp�uT�%YB��[��x�S������D���������S�'�敄�̻V���q���>j����s��_+��'�����b�]>#M6���7,-M{����;�ȟ$�>�O����tx�L"&c�W�K�G{g
�T8x��]d�^>��T�g   @�p�J?�n�Q�h#�Ãq5���B�s�%�T�_���D��;�"���Z��]T�|-��ӹT��Tt�R֣��ù���I��Q�iM�O0���ԉN$V2˳�1���d#�&���s�R�L���.M��+}d<1�(*O�ē���UM���b�2>��̈E�J&S�:@$J�+���L^�#K����;�����	    ��
��&@k�(���Fu�>e�a�3��E=����\��D���ա�%>�I7(z��R�Z�(#�ז�D��ɧ���a�4�-u�(�)Bs���3ܢ�D�ӑ�ZQ��,.޵~-@i������"��?��E�Σ��֮]�3��>   �Z�����=J�eMM?��_��ȯ�j�$J���%�ա<���������C%*j8�X�#qSO��<�L��P����9�NKK���L�d��NG��7Q��)TH5-$*_��H��
/�$
   xf�
U�D�,,g�PN
��%�]���TJ��$�D�(jii�a9O�UZ�L%Qz]$
   �H�
�~EꢆUUB!�RE�lI��U�H�Q�lBܠ<�$��Te�$
   xml�R)�&�A�즻���dI����T���TV^T��.�X&���9ݥMGG�-�-.Qo���P6���<6�j�[��CQ�b����(R	���$�DQ����#��   l�(�P�E��(Z�W�8U�;�FQ�ҍ�QT>�x|]�����*�,��֡o�+.Q��AVh�*��G��PZnx =U4�ja��EѪ�8��   ���r^�$�^���_�����F�(�M����ɔ�L��Q�u��2��'�I�ء�2*Wfs���@|����Dy�m�
Y)��������"5QrIT6�x��(    lb�5Qk�TޔD�&��&    ���:K�ik�8Gw�A�    �"�̓(ֳ<�^���>�     �	Xo���k��&                                                                                                                                        l��ӯ���<��Q��C��%�f���_�No��X6>��F~���7�}pO|�l|��[�������I�dc[ǅPF�������U���y4�?��Y�;۶�4K~���O7�   k�j����=̫�����_�B꽾���&Q_��|��JTs����tt�����r�K����Zy�����:   @Et����'�m���!Qϝ��ȋ/Q�Qn4ʿc��ق��\�� �  ���W Q���l6��4v��k@�,�bJ�ߩ<
  ���B����N����Ѿ��o�yg@��gƴ���O�9�|.|��P��՟�"w�m;� �f���L�Bv�������`,���%���{F3��[�1��zocOH��ji�jhl>��RO~��t��lH����ۤ�?mr�{zc]cˑ{�tt���!_s۹P6�pݕ9HT}��(��(�1�%������ڍ���A�}[;�	�dl�����m��h$��'iUKǎ�3��H�+�j���;#�a֐�֮ݗDx��V'{�����$�Ӹ}ϱ�Hl��?+x   (	Y�S����E���iԶm�L�Fm���FUSS{j� %O�%Q5�u�����W��B��@i�t��'%OͩJ��m�T���z�UU�kzoH�-�9T&�{��S]c��Cq�fN�/Q������ԇ�qI���:/L��'<\���E)�D5�"�D�{��?�g�w?/���8:����KT��$�
�fN쒯s�_���`�"����(H  ��G�(͜���$	����c\���<�E�`	�aM.�]
R����״H9���QQJ?��i��Z�U�D�jJM�g�-�Y-��Ӕ�M?��ΧIS�:���h���>���H�A��t>��D�)�\<�1�8a{c���w}4I<���8�i��^].�^��;{��B�d��^�%Q��=�QJja���pD���v�Q�R��  `}!�yD��C�E�%�D�(�E��(E�·ߦ+{�%��W�e:���c(~;u�T�~Ueu(�5Qf��8��/�{�EE�ё� Q���01(�4��PO��S�wy��r_�I��C)"��4��,.�-�VV�2$��P����EbQ������T�+ӧƮ=Ǹx2H�   �7�(�8T�_�&͢�DM��(sI�TE���\DQ�u��&թ�����wȹtv�D�(*�Z�P�b�QS̢�C�R��D�(*}��5��(rɕA��]�s(oZ�D��(E-.���U�2Q"�ZX���UH�*�  <H �ITw�T�kJE����(nPy�!���$J��G��}�ou�T��ɬ���@,�/"Q�Dy$�z�p�����(e���D��G���!�rME��$�I�֖D� 5�  �������X�S4�*#Q�C�{�b5Rjn�kw߁���N�j�D��q����d�(�P�2E��c��w�z_SO���<Y�������dQ̡2�:Y%�8�t���[��IrWHn��ҋ&����'�k�"�+�iYyDތG��eK�DE*˫  `ݡ�(���Y9���J�jjNܢ����y��ze`�P�������#R
Ew��F�r��Z۩��<U��\l�{zc?M��|<�O-���&F��Q��/+gERަ�s!�Y��I3(�{z�����^��O��A�M%�E�䭥�tw^Vh/+/��@ޜGR�a�w�e�F�r��kV^��ZY�@]  ��� kc�m����e.���s��LI��ciU�O��GQ
w(�Ty5��'S����~G��Р"Ώ�����G�IE[|��E�n_SO�e�MfQf�"�m�
�9�j9�;����ӭG�"e$J�g|y*Sr�(���ʔ��fC��_^�����(�Jeje��&��5/��,鱇H�ݵ�7�GSr�����A�%�а   x��=zV�     %��ˡ     @y��5�@�     � ��0(                     �>�H�(�Jo     ��    (
o\��R�0[2�%DZ���X�~��y����������x�^�+OU�@�O�c_���b������Z�$֒�~�^\ͥV�N?W��Cҍ�<���f��}̝��5�i�r��f��<�X�'������)+Mѓ[����|   ^D��<c�ɞ�'�ؗ-q���NFF��0�2,�;TY�2A�E�Iɦ#C��ȚT�Ԫ�U.��/�)�QlN���K��Eӗ$�_��v���"K1�{a1���γ�W(�D5�u~4�&�7��P::�ݎ贼��Bu
  ृ*T�1zby<k��q�bs��=q'���E�#�)97OPS[pP�81F�SS�pp �]�{W������:T69~�wh0��-��Dg��bCԢ�������PP�(�p�>;O� ���yަֳ��������$Q��s!���h�hU���A����&�����f���9՟�d��c���d��~�*T�nP�R�ܱ��&M�Pb*U���]7�   �����!�t�$QŬ)�{�5����Sy57�t���a�9\wj�{@�<�Hu+M����)��bp���N#6,��D����L�������̄��v���C����(Y�����9_�˅���2^(t�Ĕ��%�+��@��Ӑ(���h���6E%��P|e/��x��W   ^,J�P�D�,Jr(��+�~-�f�n��#��&&Q�\��W��(a��P��*,��D=�{�I�(ͥ�L�_�LU6��
�8WEI�c'��'���s�B��ˡR���z)�>�oXV��z^.�<x��/�]��s(N��M�M֚(Q��w}4�Ky<�J$���Ӌ���(   ��'g�m+�b�wFM�]��՜

�*�P"�ʆ�T�heHT�p(�%9�Ţ
���� ��"�x�J<�^�Y$�ԝ�{���]/&Q�N�0J��VOnD5�����xT��
U0���'Y��X=�QE���5��ve��]��@�j��	�  �RaO��K��(٢x���	UMM������US['�D�ڧ�%�i�^N^�m�	��q�bI�.Qz&uc?��DQ��%,���K;K͞���D�kʉF������3�$��T;.+��D�k�5��J/�|k���;)�E��>��D𢴨�  �a��r'Q�E�= 9�S�͠�P�jf���Z�(������%Q�Dq��%K�XE�&���b����+�(�� �\�!�E�<N�y�$��B͐5����'6�џ�fR��  �2a�(�E���|��O�C�(�t0���;�ؐ�Y�Dՙs(ˢ��bU�m|o(VN����s'Q�v��
�i[���S��DI��Jj�擔��e[a9Ѫ�(�eBw��؝   PX]��&ʭD	�R��1�-��eR��Q�v<^U��强�Cq�J$�I���.Q�w��(k]�]��4���<�K���(��\Z� QN儜D�,JŎ��D�6�4)B���,
  �K��a�P*�M�^�$76����S�CQh-��P��y$�%Qy53yjI�v�ݡ�E��Q����:�QT^07,��mb�����~�����'�m�KzE����������~iy�;��,Q�m�?`HyI&e|�ܬ�^��6����                                                       ؒ�Y/z�rv����'��O�����v�zOr:-�����ܪ� ���䧭W��a:�E�@\���C�ٹ�Y�e�Q.O!Ϋi����15��#������<��{�/~_|�    ^ �0�5I2�Г,�;��m55d��>f[M�;�y��g��G%����$������)��3�d��m������#�S£�DMi�o�/�Υihl����#cZ�?�7    �
�9��v@�(z����EQ�R��:IC(y�����(2Eo2��ˢd�"�d�'�iN�����2���C�������i1    ^D�CMvsq�E^�c��
�c}H.��R�NT������o����$Q�a�D�Y�/ᩉ�س�(#��Q�(   �%@8_�c%$j���w�Cm���y��硃=g������<���f�==S��S[M���(T��*��X���y(�   ^|�8Q��-�FOd%���)1��K�ը,��\��DY�s�;o{��Dq�J�U<"Q�G������\z�|0U�kzOT��,�2��$.a!   x ڤ���I�$$�YY�#j��@TUM��yf��I͞�E=g�����(Ke9(*O|��(   �Ň�6�D�n]�$�$��D���w��M\پ�&�eM����漸����>7�`0����}���@H6�t'a����$C��m%ے�J�����J�9���{�j朗 y�{�Z{-S/�8w��5QTee�bVe9�D�I�{/v��#�ʓE��^5Pe��_n���   �=�'E��9*�ګ��t���C�S��3�Շ��w��u$�/���(�\����    ���-*\��ǟfw�ؒ����w(�S�䚥Q�'�Q(Y�C)����p�걢O�鼦�O��F�   �wL�CY-Q��]���;��j�[9�l�HE�k�h[�۴��Y�1��sw0��r�7˝�r{Q                                                       `�p1�l����J�|i���GW'���דԿ<ǝ�K�G쥣��������p��ش��x�I/�D����h����{�)gߨ��=L%S#s�`/����D*s���|����mZ.����cy�pr�z�����n��L{՟o��    ��▨�.�R�^X��⌵�Ne��{��B��r����-��j���Մ�O���C��lI�ӗ��<�(��zOΦQ�$D��!��ȓ9�:�w�Ff4S��1�b��^{}��L��:�&�L����H[�ov�����G%zN.V�Zi�\L�y�ە�BA�   �wG����%�A��D�ْ�#9&O:��4?:]�(Sw<.D�4�'�1�7�(��w|�,\�ɘ�P���+i�wnpO*=A
u�g&��D��J���r%oI;�;��a�r����ɂ;��RU�٩x�opt�����z� �   �=,���Қ��!�+R�8�'>š����#�F��9�w7�zC��LI�]����N���\��
e�^�9(�w/QJ�*Ƅ7y%�	D�PT�HT��TfO/寔
U\��   �E�DQ���=���D����a;E>%,�>z}I,尕����F$�d�sWg*�8ߝ:9WqKT<�+�-ge��J{p��)��D%ɚT%���k]��N2�g]�r���b�E̥P�biH   �nrѪ�L{6�j�L�̵�C]�-iQ�"�Ȥ�[��2��Ǔ�#$J3�*s'+̋B�\����rS��ގ(Რb����B��(��IU�WZ&��7���)
FI��b(!N/H� Q   �;�+e.��6��P95��9K��/u���?u�N2�Z^����k��=$R�"Q�dzd��U�]F��
�(�byR��څ�ܱ';�gI�[� Q   �;��&ʝ���l8h @��ڧ\^Te���D)����,����*���R��(�By%�'M���2��/���H5QTee�b�X�sn��D   �,��yvmy�D��v������EYA(O����#Q�Q<��<��r���Pv=���%�nk�R�g�EP2e�������զQ+�`S��<:���]��b    ���D)���(_.Obe���q.O=��$Jf���P�O���'�y�>QL2p:���%��ʡ8��XK�fi�sǥl�   �Q��c]G�����Rq���þe�E���|H�4O.�cy�D�ߦ]��R�M��i��X��ܩ*W�㭈
�D�ߦz(Ԡb�(                                                       �+�s^���ֵձ<wQ��	t�67f���Iy4{8�-y��9�%���5�%ޓ�����=w����9�Z�����P�����/mH�2��G��B<���r�rӒL���M}{��J�I���k���6;������{2}�e����}����4�/oX��R}�W<3��D��鹪��퍅�����!?��=�6ܿ�L𩭵�Ϭ��;x��e������:��#5x��}�f���ݟ�F��?|���j�����_����+�W3��헥���_l��lo,����>������u���_;�    �ʔ���e��+��(�\�`��E�`l�r&��ė�w^��l�ПD�t�D��S����ۤ,�=	�g�[O�:.ܬ�i¢ny&����a���6�k��ӆH�jڳ�C��V���υ@�0��ӛS�'�U��=8�uj�*�^����ƞt��lU8ӫk�T�.�Qz�PWr�F~a~}��5�/$Q���?o��t?9���߰2my����d��'�˄5��ʸI
�Z��Z��̷!�j�^/,.�U��#�idP����َ����3�G9��Q�G}K[$Q��E�| L��������<�>/o�?�����  �_�;i٩��9,*[��I���d��ӯ�6�Mq'�Pw�uS���I�۵�j�0�+O�9zw]��o?O�̔�+w�XT<��+���Շ�CmT泹F������b]E��d��r�4�sy!�N>���=��y4�wz��	L�C��?^�?�-���(�wj��o�Z+!%�컺̑)�&ɟ!Q�P[k'�2[��ooQ^RC����ZTj��O�f�ۥD�C-oo���G��>�yP�^N�  �EJ�Q�K��Q�$aO�b�e��X��6�#�M�ɐ�o��S�(%jB����c��D��۶E����'R'��m3zR�j���KK����ӽ���=I�Z��ne�⤂Qʩ�dK׽�v'�0J�B٣P��u�\"3pf�d��%�QHk��2%�~�.�BE�<�Ps����e��qF��{���
DŔ9!  �F�e����9si,�s�R�(c}�Yi!Q]�يeM���x�P1�T��UX�Tj��!�@�KlQ_ȻT�.�c�h��S�z�Dfb�V�>1����BJHT�Ж�O*��xK���(
G���Xf�4�I���8YyS��2zᑨR�����%Qb���bYJ���%Jš�>�\-�:���|^cs5��o�J���_�YA��(������d^�&
Q   ��@���I�J��Y��J����k˭�(���4��(���}D:�:�K�x,�r�/�aQ�3z�T�r�������9�\)V����(M�^�CO�LhRO�8Lu�I7Z����)�&�j˯;���D�H�J��P��U�YF���v(v'Ut��\��-���?����Y+��cؾ)RR�^��R����������o�  ��bIWC5+T����ZK��x�+��.�L�'�2��D�Y�<y(��⩌v幷��%����6j�7�z�\}�6�	=S�zq+��U��F���v�\�sL/�78���J?���3=�=�[�%�z|(/ BaE��B]�Rx¢�^�-�jO�>2��r�[Y�5JkoQR�8�����tL�9��5J�E  �ͱ%�Eg婉
%Q��x���uL��Ӏ�;͌ع<���OM?�d_�D���%�0
����r�}��j���F��|@oczTM�I=�C��,�l�&*�[#$���Q��!Eq���ϐٽv�6a�<Ҩ�B�J�����������˥�n��ߩ~��{��  �-��}E
��zr��(^�t�p��c�\�Ĳ��㔾k���l���+��)�>���KT���r�+˽��򪭁
B)�rѓ�r�J��+��y�����5G�8 Euq���P՟�}�TP�ȡ(�����ǢB�pT��DJ�=��b+�������˗S�*�z�  ��.Q�fS��y����O.��挞fГ}�}c�x�>ع<�Lۙf>Gz�9�ge�EĢ�%*�H�N�����	n��q�(MZ���&j�zH�(��@ʕ�(.�*?����I���O���D���*)Tȹ<I@��\�����n��lK���Qu:ύ,�򆡔C5�����
���%Q(-  ���%j�˛�F����s%w.Ob��j�3�`p�Է�ǢZK���~��ϰ:D��A�(�\�;��F5�f������W�T,���%Q��eo� ��eD��Ǘ9��+#W���ѱ(Y	��U[]�.5�]T��6,O��н���DNU����*�dL�^�@                                                      �m�9��i���4s�䖿c�ձܻj�����;�X���qyv�j}�3ꥻ'ybN���{�r�=R_�=�FA��-����T��|��k�<�/��;�����o�Q��c�L����3&���t��~8�}����9�;���W
����C��z���N/s�T5q�!ٿ���י���kv�����|[�7,��i_{q�C�   �c�)-���.cKTGc_�8��Y��	@�缘zqjؚ�b46�c��<�W���i �p��F����i�K�0�ssu�0�ȯ��/Ur�t3)T�j4���ə/dN7h��Ϋ��gH��|Qȓ{Hq�弜>L��]s�I��B��Z+,Q�i�J���/o(QdP�E��َ2���^�e����<~ޞ��Z������Zy��?����Ycs%+�����g�(   �wҲS9s�"]vgKt�#�"e��d��ӯ�6�Mq'�Pw��óE;$E��v�1/��Ky�Q�>N��uY;���d<52S���moQ�Q*�t4��g�:�>E�T}����{�^���dh$�Q+߷�L�7��쫗lso!�F8��4�(9��|⨔�I8�Ej�3�5ˡH���y2,U
A   �n�uT�R%{�%Iؓ��� bF�@��6�#�FSZ�}��S�(%jB����c�ԄX��Ѷ-��	���x"ur��IF/�%��4�R�PV
ES��a�¢�\��N$J�:�����˧f�K���kI�!R���ڼ�pR-� E�������Թ�Q2��H  ��
�K��Ӧ�/�̥���%JE���ig��Du�{Ff+�5Qj��C�8R52Wa�Rq��{����.�E}!�Rq(���y���^�J�Q]�L��8T��C�X�N�Wv&Q�*5�~�iiP�D�/�N���v%��y:�S e��֞_��m�0��<����OH�  x/�q�*'q*ig�v*Q�&ʮ-�֢$JV�;��B�����P�\.��(ˡ��.�Eu��#��D^��z��h!Q���r�c뺓�(�-w~G�:���z��������n�D�X���
?qI�SM�j���%���ay��J   �	�Dq5T�BE��^n��Dy��91(uo�DuIej<���M$j����Cy|Oe���s(Ͻ�Y�N��~�}�#Q��y�'�Ǵ�����3���z;�(iP�#x�Q������ם��R��a���byR���  �aK���$�S J�T1T��Q똞��/
w��sy'ş�g�d_����BS�ԣ�����r�}��j��v��k���(N�M�T���ې(��@�Z������:-,�^�0'�����gf�U��^   ����}E
��zr��(^�t�p��c�\�Ĳ��㔾k���l�:�FU�� �0'�Q�'�C�8�'��-���א(���?�rW�T�\u��m�P9O*9x��x���z�S��a�e��t^����L�   �n�(n��Mͼe�R��'�wsFO���>Q��1}<I�\�D��L3�#��ǳ2z�"cQv�ײ*�������P�_j�0T�ג(J�Η���HTg�M���6�C5�C�*YT��'��@�   �o]�vܱ��it�<Aa)j�9Wr��$V�F=��L}�Qx,*�����kwٷ����o��N��6�#$�M�rG�ȢN�;��K���
��R���[y3��fD$��PՀCNU��TD                                                      �U�9y�,Z�&�N[�����}$ؖ�ԟ^����9�X�V�̻�qj.Nmɇy���)k��ܓ�w��=煺���ҷ������v7z�E"��\h0���ڏ�zG��/Z����giq���z��!�;0i=�˝��;pr�:�o�����    �,Q��/r�ITW�x����#S����]�v�-	yr�y%J(Mnx���/�q��',��iFc��!�f��\Qȓ*z�F~nn��F�14</��V�|$g�س�ĥ�&�Q=i�+�C{�L?�t�Q=�~aIF�|�s���֨�&��(   `�-Q]��Rpvi�{��D�Į��uK�D�{�y�Q�>N���ˋ�(v(}��xjd�\_��S���2�4ǡ��XS��dN'
B��a��t�	�Uy>�Ϻ��bP�t���%2'�R�(   `�!Q����v�4��\��V5̓������K �D�1��I�E������s�2zn(U0Շ�Z_ J��X���š�fӨT�x;�����j��D   {�H��<�y�P��}lV�D��٣����#�o�(�� 4}7�K��C�"}�;���PkWB���?�d^���/�A�z�ʕ|��*��*U�M�Q��'H   �7مD��{�խ��W%��P�D)���Pa*Q�C}i]��AF����"��Ru[�,�R�(�G�����ɝ��t���ϣ Q   ���׋D	ҟx����H���v.�E=v^&Q|.�9�Ǘ��{-	��b�@qFO��P�!�N{ҷU5y��)'�*4J/o�+�(   `oҺ&�2s4����d�g���mj��2z!%CO�br��=��	�(=�4+��#���䯉*���2#�ء����kYRV�   ~/�8�w�+�}��Lsc氽���<myP��2��jɱ��D��]�]�KdQ-������@*aAyO�UM{��t^OF,T�gUg
��1���� Q   ���U�(ne��>Q�0T��>QM_�(�DusNS/�6	����H���5�=�WVF�Q�X�܌�����R�'.��,���y����r��ע8�Y�K�(   `o�B�8�4�jXn��vб\\��أ.�w,�s�����MyC�XTci<�c��K�Z����X�֣V�(
C�WE8U����ߦ�1�-��"Qr��mڕ�V���X���F�_                                                       �[f,�o��вG����i<���uuws?sg�pw7�y	������f�/4i�Kwx3���b�D�;�[��y�u@_�;�H�63���𿫃lYn=���{���W�;����W��p<���t�t�����k��s�   �;J)�5'/�㞝'���fg�F�3��7i�p`��5�8����I�+�g�$*nMv�k�'R#���-Qs�6�̗D��5E��I����+Π<�&�=y�OÊ�x�B�@�����(9��   �m�H�P��\�,߳eI:��4?:]q��ٻm$�[��+�9�]l!Q<��D1(ߔ��H)Tި��k���q!L�J
�Z�^��r)�D�C彃��N,T���|�{�0_�aP   �^��D)�*�8�Ĺ<�x����={��Du�{H��C�[I԰P��J�*�D�8�Wil>r�e��x��K�+%CQ��2z6n�J�N��=    �5ZITWױ�fz6U�꣄/�GoF��Du�{F�w��oFK����	�����X�7�DY������R�
�:K� qZ�k��Yq�ZnҮ�
)�   ��O�Duuɖ�B]p�)��(/آ<�%��r��E�D�d��}(�Hl�5Q\e
����PTE�N�)R�cv��#R�TB.J�����̅G���   �Q%jJ�)����E�|(�4��\wDH)�t�h<	;B�&e군�w;,,We�k��/�M�Y�=���vz>�I�L\�&+(媈"�*4�/nt��    �;A�D�b��=O��P�f¢�rn	�(UU��;ͧv��Dia�K�:����9H��n௉*�z����ߠ�2%�4XV�   �$aeד{�E�6p���^�mQ�E
��z�P���t^����M%�*�C�H����鼪Q�<�2�2�����oT���^��\iU��   ��E�D��y՛˓�3za���O<�A7���j�<j��M���6�N�5}}�ܕQʡ�^�r�Ǭb�~�J�   �=FP���;���٬p���@c(w,*(Q��<�����p�˻�s{ԅ]u,ww+o�R�j3�Fm�rvNUyh��H���
��Qzy��e�M����                                                  o���      
�8�ʔ��wd���iO/ZOuuu��h�4m����_�j<��֭��E��xObܾ��7����0F}��A�z"O���JO*=Q������'R��������=I�`���[���{�Է^����+���<��zu�PO�t���G]��,T�Z釳Υxd�千����C����?_��������_�g�z���?{�z�Dm��<p��Rݬ����������o���j���   �7�)i٣��]�:��\#W:�-���p(����	��k�a�2=z@�����G%�hl����M�}i�W��ʞ��H�/�^ߤ�x2}"[5���3^2'拍�����@�9�7HYzR�'�S4/�%�>9���y�(��G�t�����Vi��W���U�F%z�O-�m�"�:���r���}o�uu٬W_�J�o��\U��X8��_�F)T�))��L�Ƞ��g߳����gn�r�'�"��  �}�bN(�P&'���ZU�������˙fe���X�V�����a
K�z�q�9x.���%[��II��z�R"��(�FYKA�+'���C�)Iyzr)R���](
grN�"y�2�?:�5�~�)�L���eR(uo��J���>s������D��配���L��}�9�Q�E�kX?�ߩ�[[���.�L)9��t�V��>8s_���Ї��/U_��mGo   �4��ӲG=5Q�2�8�%o	�(�P�¡��Ǻ��<yX��B�8e�w�I.
��F�5,j�b�h#-$F8���9��
F$*Aa(��	Mɩ�F���!Qk��t�k�p�-�
[����R�|�#�*ٲ$��@���~)W4���P�p(wPX����QJ������LI)�����H   �p�)w1敨.
O�;�?�=���P3����[���%��P�oz�Sz#s�N$j}vdB��fg�ɴp*OJ���W�%��Pي'Eߑ�=5_������7�O*�)��e�(��I�/����ܵO��A+ ����u6�;xz��Cї�}�Pn'Q�B�圞۔l���sz��(��56W���6X�4d�   �g�-��T��3�RU�w�/\ZX���8�v.Q��X�*�PX�dz}�S��B�4��Z��v Q��W�s;�(J�]�(KP�����O׬�'ˡd)�mQ_FK�V����G�H�8i����_�zqڕD�B5����+YD�   �_�-ED��������H��˛�j�����F�(�(�Ӄ�T$*�uz��4�zr���r)��{ti��(�B�$ʭP����}dP�U�*�  ��XG�Bj��j��J�+�g-ر�]�D�EOO^4�-xk�4'�GG���4�����jt�_V�׷W<�/�����S-j�������D9��2U�8š��(+U�ib�j�Q}q���j�
�d�
�(�B�X�T���D�i�2,
  �{749�g.�Z�$ʓ˳�,����<y/x:�h�ދL�O���!������&��y	�eN�	�z9=y:oz���N��e1�zs@�<�<���m��I�,�����zT2O���r3�-�����f�e�)� Li���ǔ:2�$
  ��	g�\}�輞�4����(j5�9�<����M�(��i�=�'�m�͐>Q����*�W��q�(�������C�5�Ը�f�>Q�i�1or�(�bSN(�/Q�̀�Ȝ���"g���=�����fD�)$���(Ǡf[���j�t  ���aOg�
e������fn��lɝ�S7�X��Xx�rW20��f��i?���߱<�H��Өa8G��ߦ�Bw�(uwH�͘�i?eiS�f�1��s��H�%*��@aŢ��F�;��ag���P��j��ߥ�>��ʛhX  �=��                           �w��9��
endstream
endobj
21 0 obj
<</Author(george siozos) /Creator(�� M i c r o s o f t �   W o r d   2 0 1 6) /CreationDate(D:20191129203412+02'00') /ModDate(D:20191129203412+02'00') /Producer(�� M i c r o s o f t �   W o r d   2 0 1 6) >>
endobj
29 0 obj
<</Type/ObjStm/N 43/First 324/Filter/FlateDecode/Length 800>>
stream
x��V�j�@}/�����J�(MBK�1v�!��uLl+(2$�3�q��X�>�fo��eGǲ��rₜ!���,��9�[�l0��X�J�
��w%����LE�P(��������a*9�T�
8�/�!�Ö8'c#[8q6���O�#<fX8�a���!Dm����$<e�	�M�� ���x�"G�dskI~� a��s�[��bJl���ŰB��b9dxt��$�Q6Ά���C��]��t���ί�rה�������O }������?�$\*!׋�%��0	ٙ��LB~�L�T�=�i�|��uC�v��3��?fA���\��K���*�����+� ��Rdq.�KT0��At�z>�lޤ��*�B�C
T�L�U��d�甪qʭrJOqJ]�H�T���K��>��~��l�j���^�l����̥:+������4��".��E�o�����5V�S�հ��f�+�Tk��+�W�W�W�W�W�W�W8+��++++++<(<(<(<(<(<��״��V=.�GM�e�f/�Qe�ްnQ9���)ZP���A|���3����M��<N����K�i��q�tٷX��Vǂy_�g�8��%BY��C�͚�f�v��5�ُ���i��׻��ǻ;	��.�I�lͿ��5?���f��0��n��Y��cӶ^l�w��`�x��F��i�/@V�:��=���J��[o�9�7w�1���$ٽ{	��w�������T�4b�9T?��މ�y#�FY얖�ĉ~O
endstream
endobj
66 0 obj
<</Filter/FlateDecode/Length 544>>
stream
x��TM��0��+|�V�ؖ"$0Dʡj�S�'Ej ��_3ϻM�R��Hof��aOhv�n�~��vov�n���en-;�S?�f]�.�{n� t������n8��f�¯.yY�+{*��`?�繳s?���w�wx�2M�����<g�=�}l�O�ٲ�hϻ������8+�]'�8�bڱ���i��'l"��l�uOء{�K���W3S�p�Qģܡ8�	e)�ld)MH�R@	�2"��H��^�k�W�\𵌋��W#/�r�Q�Rh�@�@%��m��oH��$FuA�D ����ݢ��R6E͋��FP h���IЦ�S��H�#�Օ�^P/Qr����I	=R#��,*_[ ����.+_[#�<��ry~�-�
�)	L�Y��Lk���DS��*kP�@ҏ��A�d���]�讆M��7�(��q�pQ�E#��.�zm!R�nn[$�-D
�RE3:��iF�Ȯ�pw�������@��mɍ�]�[��_w��Fi_��-Z`�E����m�M㴲��,WT�
endstream
endobj
67 0 obj
<</Filter/FlateDecode/Length 58774/Length1 147992>>
stream
x��}|TU��{�I/����fP&:�HR ����Ih	)C1$��fEł{	�d@Vt�{_Wײ�eW\�|Ϲ�HXD������߼�3�s����{�=�(Dd���JsFe=�\�B�b-D1���u�_V|AZx)Q�w���~�?9� �؄V����}���D�s��,_Rk߳�݁D��Kd~�j���k>���%�tή^^5���9Dw#���T�U�4~��"�o�8"��$�g��u���e��VnA�K��;���}Z}K��"|���e�zG�B=r�}~em�5��XB�c?���ͯ���$�����E׶Xi��%��T.j7�K�����$�"h�'>��xf��C�!��=����$���t��G�C��O
%���.���x*lǑÇw�02��;��ړn"-�\k�t�H;�j��MN���b�n���Wi�F!�E�5M3��3�ݲ���4F ?�n'\��!�-�N�E�����R�)��h�+��7��~��Jh�)���$V��v���m���D{�t湴-l��~�6A��Ns�Sǘ�Q���g���D���ƪNѿ��3G7ꃼ��������&�I�柲��u���m˿8�I��3-;�N��1Jk#�y��6��S�
��L��B�wSկ����O�ȣ<i&R�)�S�6}n�ϸ���4����%�_���U�K�m�oѴ3�����v}���.x!��3bK��w���Iڹ�t���E)�F�k�z8��I��%gw*;���t��/����s��x���Z<b���^����RLPmo��?�%�����[��^h�WO��S�1��֯�K�mr~Nɦ���S��s;J����ޯ���wۯ�)ӯ�.�fx��3m'ek�jm��c�f-���F�WT-�O�#��6MA��rd;��#�}h�������l���������\`���?<�$��Y�:��3�>�u4T�1�/�=k�Oq^�L-��`����~����y\K�l#��z#����zwJj��S#~�0�xoJ�w�v����!�u�������T%�[ �O-E�}�B1꽣o��=c ���O�|�^�{�����u��6��+�@e\X���B��M�~Kh���8�I��R����6�_�5?rO�w����WQ]��N��~a����bi	��y4M�ө��J��A�6#7�;�|m3_Fڅ��"`��M�V��b])l]��X=WzX3�U~�f�W�/�b�C�3��O���w�:`ůŝ����M��f�F3��/�Y@��.����1��@0��2.�f�g��y�c?�I����o�I���=��u?���9e��4F��3���{h�����U�#T
x�/m��)C��Z!��6��N�qX�~_3=����ǩL;D��/�b=���Uθ�ہɬ�g�i>b�o�Q��.��k�l��&S���#�Em��I���,`X�����_�?c�ŉ�-���L�����)~ޔ?k��sf���,`gj��՚�L��:�[(��K���,`X��[L��O�,`X���,`X���,`�~�Q,0HR�_��Y~sU4�L�����n��_=��,`X���,`X���,`X���,`X��Z��G���Φ�щ��v'J�t�@&m3��"���""����4��R�P>M�B*�b���������v��Wd���M�f�
�*�z�&��>�y}����fRZR菉I���&Or�C�{�"{�}��┗��Z��'������Ao#��o��2��Q�����v)zۮߨߢߥ7�/��m@��6��-��m�}z#�&Za
� ��I��1�!ˉ��R�=���#h jI8v�f�cm~OІ�_ol�u�ۧ�>��O7}��㳈���K��y��g�o�?E��5���h��6�V��n�7O{?1>��wU��p�5��LC���t��p�6���B��":�΢�(��BQ'����B�Yl׈��^��G���h�a�-Ssi#�,-G��Fkc�<m�6^�����k����*�^��j�%�Rm��B[����jh���m�v�v��Y�Xۢ]�mնiWjWiWkڥ�v�n2��&�)�l
1�
��-F��OA�G�~<������;�F�7ni��	��F_k0����7���w�b�n�����:��SR�
%�ͧ
�����ֳ�����{�V��+��o0����}��}��>y7ϼ_Q؁;��D���kל�h����̛;gvUeŬ�3�O�ZR�qM.,�4q��q�c�ƌ����5ҕ9��Æ�<h`z�^i�SS�:���b,ё�a�!�Af��	J�q�ڽ��^S�c̘^��(������k�+�m��^j���F�YuR��#]�#��>���J��8�ޗ��fQR��ޒ�(�{z��M�F!��d���$�ɶ{E�=Ǜ�dNCNi6�5��e9�*�z�QSX8d8���cQ��>BB�3�I��H٭WO�)��N*��d[���e��AY�`#�}�3]doJ�۰��B�J����i�^�FzNC�Fo���Ñ����D\r�7͑��u:�,��x�kN�8���w<��S���X����O�&�#��%'˱\��Y(x�<\��,��\��b�V*k���x���W5Ǜ�:���)�/��譟e�7�S��z�WO-�U>GrYe�#;����ueC���ך��'�e����r
<�t�"o�c�a��`�d��������r+ozN��=��4�(s9
<{����v��ؒ��8�	Y�)�9��*���Z����&{]Ř�b���X�%���c?�K6z4Z��N�V��ʃSB�ͪ˻�=�Q�Qa��2��n�+�0�⏐�M���1�J�M��X����N3$�L�oH�\8�����šq�P{Nev��Ij�П�����\�;F�y;Ǩ*=+>i����v/M�{��b�!�$��69���͟��/(�w����)q}����jUв��:����F�xq�I�y��!���P�Dz�|��M�欋�����,�#Y��WZSE$�fa��b�s�9�Z�m(kn�����r5,�)�3���W����n5_�Ym]!���|�_4
�4���
�\b����}S�ǧ	-�tTqSW�y���0���J�,�eAf*D!Ĉ��q��&�a�˛��Tެ�����p�-o6q�KE��a_=Gw�G���"k"�HȨdk"9��0�+���"5L�t��y���vE�HamB�B��,�B]�=F�Bd="����#�a��?�p��+p�xvE���%Oa�<Cx���+��xNCi��=(�*��W8F�Ws����"�a��Q�p�(�ϔ�L�I0�|� p���P��F��!�൦˔�斖"O��փ��XKӀ�7ԉ��9e,�FK��=�[_^&�An�l��W^�u�"$������5����F�x����[G}���);��-6֫�KcC�A��Ӝ*;J/n�u�36������B16��a�EtV̓���;PU^j�gd2�2�,¬�ĞoJ�4f�W��,=%<2��	�-uxo��S���y�Fi�? }[��Qj���7��*O��1T��LS�L��e�:堍L���F��������qd��!r��x�����#0���[�p,One�;��O>d݃�J�';�S���BN�F��S7��
�<ΆSK)�o�|���͞#_���M��������A�	tt,�d{E��'{�/�VA�5m$o�S%�/��l��n[�s��+��`Jo>C�R�^�ge��[�'S��;bo�[C��h<Z�7����㏧N.��r�gv$�-m�m�G��2���{�.p�I�u!�� ��o�${i��GSQ�IN�b5��U8�:��`_Ϥ�R� q�I���Ƌ���ґ�7�W�@<�r�&��!kC���k��\#}*�]�$|/r:�*��J��+����1;2�5ǁ�\	�1��8l}��Gy�<�O/ub&bb�C�O��ÔZ>��*�F���̊&!O����CSd /9��Φ��)'<��B'�Y1�B�w�
1֓�:�Z�Tʋ�%�O�:���Se���^���=F�<�Ԫn7��x�����zM�bNя��>r����e�M{��R��>�����������o�� �~�8�1��G�M&� �qU�
�	��d����')� j�m�����Vdd���McqC/P�|%�S�^��J�Qb���X��
%�+�L��J,Q�N�Z%+q���X��%�+Q��9J�Sb�s���D��JT(Q��,%ʔ(Ub�3����4%�*Q�D�%�Vb�n%����D�JLRb����8%��D�c��D�9Jd+���(%F*�R"S�J���p%�)1T�!Jd(1X�AJTb����D_%�(��Do%z)���S��J�P��ݔHU"E��J8��D�v%lJtV"I�NJX��D%�h�D��J�)�N�X%b��(�D��JD(�D��J�(�D�f%LJ�JhJ%�/D�ǔ8���JQ��P�'%��ďJR�%���_��^���V�o�8��%�V�/J|�ėJ|���J�Y�ϔ�T�?)����X����P�?*��+��*�o+�o*��+��*���xY���xQ��x^��xV�g�xZ�����O*�{�x\�ǔxT�G�xX���أD�*��+�[�]J��hR«�}Jܫ�=J�T�Q����K�;��C�ە�M�[��E����I�Jܨ�J\��uJ\��5JlW�j%�R�J%�Pb��+q��*�U�K��X�-JlV�"%��P�MJlTb��P���=B{�:�u���#ԱG�c�P���=B{�:�u���#ԱG�c�P���=�F	u���#��G��P���?B��:�u���#��G��P���?B��:�u���#��G��P���?B��:�u���#��G��P���?B��:�u���#ԱG�ӎP��N;B�v�:�u��#�iG�ӎ��%E����y�gf_�x��\:��y(��Kk���:G�Vsi�J�L�}I#A�|IY��LK�긮�K��j�y�/ih�B�2����_��<��Ls�f3U�:e�*�T�T�4�����i&�n7�KӘ�2�03y��f���f*b��T�T�4�i"���L�����y�<�1>�X�h�\�5�㳎e3e1�⺑��Ŕ��F0��4�#�1��C�2�3b��0��,���2��d�L��]/�4&'SO�Lݙ�q�T��ٕ��ԅS'3ٹ���3SS'&+SG_�	�L���A�����vL�L1\ga�fgS$Sׅ3�1�r]S0S���$��ס db�٩qI0�A���"�r�g�#L���\����L?2�%�~�%N��Ke���;���K�0d:�u_3���_1}�����g.}ƥO��'�O��s��L��C�?2}��>��ǥw���?�����[Lo���י^cz�C^a��Η�^bz��y��9v>����LO1��#���L{��ǘe�#L3=Ĵ���#��L�3�f��K��|	SAML^����e��i'S#�ݾ���.�r'�\w;�mL�2��t3�ML;�n�d7p�뙮�k��a��t57��KW2]����.�,�1]�u[�.a��i�f���KL2mb�ȴ�_ZZ�t�/�
t>�y�x7����X����aZ��Wq��L+|����|�R�%LuL�L�9u7?�i�/����-���L�L�0�c����0��Uq�J�
�,g��T�T�4�i_�t�4��|�%���;�0��Ý��9K�d�B�_�4�'{�苓��_���^�q��4��s���������ŭ���6��}qkAY��z�(_l.h$��)�i�/�wq���b�AØ��b�1�)�34���Ŕ�r� ����4P?��닑��#�f:Sonދ{Hcrr��L=8Yw�nL�L)�9K]����L�dv�bc��풘:1Y�:2u�Y��}���>�LPS<SS;�Xn�,�f�b�d���p�cg(SS0SG�9��N�IcL�j��e�8]n;]a��p�|?��w�G�������Q���8��k��寀/�/�ϣf��5���)�'����?>>D��������w#ϱ����6���jۛ���7�ס_�t�^^���e�^��o{��硟��g{6r���9��#g۞B�? ߓ���e/>�8��HD���Ŷ�"jm{�f�A� �G�n���4^���{�W��	_e������v7pp'pp;p[x/ۭ�[����&���sl7B� }=p���urmG���
���\\�v�"�ְ	�K�&�.�m�v�ms���z�m��a�@d��w׻�k�w�u�v�i\�_-�W[W�^��q��]�Aa��+�+W������5.u?�m�*m�k�{Ic��TWW[��P'�Dv��S'4������Zw�{qc��j&���xkLü5�k4�a�-{w�X;�]�j"-���5.t/���͘��8�]�Q�l�p�g�r�e��gfLw�h�Q��X�.���F���"����=9��]�X���1�=����q���c�y�cܣ3r�9�x�d�d�[� &t�H�*F�������YMd�Z�Z��莶�Z��"kb�����tУ_I�\�=�r�ۿ����߶7�s���;�,	�=^^[���\�3���4�Ֆ�H͍���x-��x��ta���� f�����
�G�$�V*r�7�Pa�7d�T���M�,?]%ޠM^r�L�4	qq��g�q����[�PҨ|o�d�O߱#iTq��^j���-RB��3�-vz\gQ����b���-�X��h����1��([�&?Z�tWT���ё�HM~�D�	�Hx��u��T�n�ܙ��5WxfV�+�W����]�:�gg�|�X\�4�Q*u��^���e�Ug��yZ�0��ŰZ�=}��t�� ����$��mUh ����Z`�X�V ˁe�R`	P���s�E�B`0���s�9�l�
�*�r`P�3��t`0(�p60pE�d�( &�	�x`���1�h ���,`0p���,`80
2��� ` 0 ���}�t�7�H�@O����)@W�t�;`:I@'�
t: �@{ ��v@,X�h 
�"�p B�` 0��-�� Q��O�?G���?����?������������ ___ �>>�|�>>>�| �������	����
��^^^^ ������� <	<�� �������n`�� /pp/p�h���� nnnnnnv 77 ���� ہ����+�+�m���e���V��b`��h .6��z�Y/��ֿ��X��_`����/��ֿ��X��_`����/��ֿ���{�� ��{�� ��{�� ��{�� ��{�� ��{�� ��{�� ��{�� ��ֿ��X�k_`��}��/��־��X�k��އ�˭������ŭf�g� ����]����L�y���񵁶���8}@������n���KO����i�&�o�c���)B���Q�ᖃ�n��Q�<����d?�i��|s��c��X�5�R��6R{޿��-���E�e�,k�����p�cw�4TBSiM�R*��W����9��i>-0JP7�U(�D�C��ZH����:Z��EЋ�%Yw�Q����Zf�}����V�?��U�Ya��kh-��yt����ZG�q�6�&������6�>_L����Ҧ�_��ex��t%]���Z��$�U����n�3#뮀�FC��G������c.�1k<#j^��9\�9X�+��Ոy����5�vym�+]���Z,�ϣ�� ����̲���؊k`}⊸t�q�'��g�t^5׵��k��T'{I_I�cބO9�R���FC���p<v�Q��n��p/�0�b��}݉�}75�N|�Э�t�q��D>�E�q'�����T�]~��g=D�	y��b�y_��(|���O>.?I@YFq�z;��"�D���(�3>�C�Uz�ޠwD$�k�>�ҫ��(�F����0�������N6sG��-?�,m�ICU�ȝ�K�i3~b_p"R�(��'���-?���ݏ�o�s��oɌ]s��:v9��i��	t�w���E┒@C����gg��
~'��8Ä�Y�h��`ǎ��m�c�E�ݙ�[p:�<���}�G?:;$��H��>�|�/fHz�O���o�+�c��h:��`�@=hK��)ۻB�3]Z�j$I�tv��ܗ���Dg���"&9�@\����[�-uP���Fh�:�Di�o���#���:kz���dY��\�O<��qdN�o��1:.2ȬuJ��5<�2yj���I�zp�n	�>xT���.��$�'$ņ��&%�'���u���#Y��#���a�2��W��h����ΉzKΛ��b
og�I	����=���N2G��x�ut<���rش�G](��(�}um�rw�E�s4�Ejs�w��!�pu�*�"?#�����]���p1��#5凈���.I��H�`��K�v��q�+�ለM*�u�ݔ��;dHz���1��@����ӿo���;�VWg��H���u��yU��i�Ȃ����dܱnz��;���,�6�v�ɦ�aI��Rڅ��|����))%Z��)�C�����L+���ɳ�Q&=8"T;�|hd��eM0�£Bt=$:|�ѕx�w��������[WG[�E��Y��G$>#�a�L������1ޅ�x�����dp�N��i28M�=���e��Д��i"����s��?�0��]�5�+rG��p-�c����j�����"�)��2f+f�H���1���t��+�9��\@a�v��),2��jKA���F,�L���f�L��.�cꟌ������.����rڝ�&a˘X~nޱ{����^��n+���sജ�ǎv�(�{*�pP�	)��)�wx�'+U,>kvሞ�n���ҊV��]4:#6l`�M�����tǰ�G?�n;��ip��;�e-ߙ"̝��{ͮN4��E���,������Ϣ�1�?v�D�Nɔ*�|�&�=i ���B�`�y�H�鲼�f�)9�Y��Nn��,�vW��<��,z��G�O�j���=唐�k\TP��#(޿��=&>��&gK>���皹2o͋���|�kk3��ZC���ڗ��Q���>#�H��h�%۲-[r�ț�Ķ[Nb��!�1���	IHhXR�,�-P�Z(m�\z�G��I�҅���B�������M��+
���@��sΌd9	K�}�4�9s�����s4!)��̩�{V��w�s���W��m��F�<!��f[C�s�o~��g���l��e�j�ʆx2>p�n��-�b�#�!^@��@���� ^����V\G+��\\׹��V|��r����S�p.g�5�?�_���KP��8�8�T5pbϵ �$�cQ�D�au�� w	Z�`�Y�4����̂�Mn��a$.P�HH:�<@M���P�m���i�Vf�#�n� �W8g2Ry���i��Y=6�G��WD�lUD���I��k�WMb/C�f�mxD�!t�2A�L�! d^g����C����Fp��Ў�X��?'�7Q	||�9a�|?��c�@�r�g�E�[ t)��>!ց^ |�s�qL�ګ� 0���lg�� <V��g�*���r)A7�]a���.w��#�-�����	,M�G�����1�����;S9���7 �������s��N��t�1pL�ǾAH���3' nFq�@�8;�:	f�h��)�*1�CNw���Fɞ{�=e=v�g�K�O�G|�Ș�i<�D�6��m��T��9�sx�*�.�Z�k��1?Sa$��,�����]c�Ζ0��	<玴­AQ��l�Gn��f�H� ��@G,V��2���"�1f�˄|�6�݊"��&���B�M£�Q��Q��Q��Q��Q����`�����gL\�
ي����Ԁ��F�"����ETSg v���A���H��-G��O����)JPfM��Z��녮���]�7�&(j[���%���hp¤8���?��6Lx���ʾ�}���ՙL[\.E�FѡQthE�F����m�`���}��
#�F��*`
97Ԥh�(�r����&P?XWqY+`Ki�h%��$V��Lo2��\lP���Z�d��DpH� ��#5�C�X���#��g��!�#�i���lv��'�y��@��*�u��4~�W1�N�Glm���X#KR �Z�H����QA���'��7�y����fZ�z�'�[,6v�i�?M���M�݆`�[ZR������)Q�G���D��Kǌ-�8�������0�0_�r2i���.�ESJ����~@��3�-�7u�ɮ�:�x$b/_\�%��.W��5)c�x�'�]��T��M�A+���D�����o2�.<<t��U���������A�ԕ������6�� D�'��s%�U:�S���xm#TM��i�H�4�9Ck�nlٯ���uޯ�/�N��:����2bn��emdO 'hC����z���fU�Z^Yq��Ă�ffl�bnE�:��}�'w�����N�;p,~��v���dCl�g�����z��/�=<9��[�?��W'������oݽ�{��~�3w�\v�7����>�u/ր}	q�(�O�ѧ��������Se�9%��	/�`���x1�n7eL�?j�1�I��b�쉁WS��vx��� ��H�� G����������4�!7�
noٱ��p�{|��K�_�}0J>��kz�-U*�:��n_}u�y�L}~JÅ�.X?�-�)~�E����:�\;�\;��;��tm9� ����G���(� J:���mi<�;��r�^0�c�Q���ׄ���N v�%�SA�ly\՛B��f8g'[��s8����8e�o��c�J��3��_	�xj�����\A�#�-S����G�o�ۛ�m��\y��;�~��������� \N[�x62��*�O�4iZ�~׊e�Ww�̉�Um��E}��N�)C�k�� ���@X��'\9 �K��VHC>���#�dJ�����G}�&� �z!�lB<	M��W̪���*�WCC�D��g���cp��s���O�^�{����o�$�,k50�V0Ϸ_���א�Z��9������/�Ƥr�֊O��W�~]�+���s��М1��'o���`��S�ߔE��?��&|K��+�G�1�����6�a_ .QB�k}�Bf ��y�aIڢ8��D��P$P���L����.?�76��s�,S Ƀe"����ԍy�Q�fP�Pu�'�߹З�>V��@�鎎N���R#Tv�����C�:Ou����%y9�DD���Z�T������S1Sk2��Y��;�����ȕYq "�y���aQ���̏��q!f�#����|p�n�cu����0���^E_��B%ɚ��Iש�R&c�(⯴�E�B���.���h�H�!vqq�B�%�,)�B�:G��sc�Q�z}3��;(���#.+ϑ#��o�q����`(�� p@�^;�,ofI�T���l�O��2x�*�ח���K?M���QX@�#z�|y%�۶6��eq:�v{m���ippZ<�Ҫ�m�ߢ�N�˪8ͦ����?T9��h9��oz`�Բ���E�6�~���Mr�#�Ʉ�do���c�e��nO���o�zIڇ����¢/D>���������\�����zG�;���pby����#�u~�7�۩Vl	����#�rF��nҗ���n���6��`[k��4�/9����D	��p
�i���>	50�Ҷ6�m����QA��*4T��ޫBC��)�+':�#��o=�&Ǉ���,�N���6%��_�;�[ob8���/���r�������?=$zCJ$dU$.�wnxb���i��H^�/��Z`�X�V7���a
a��3�i�z{�"i�o��:���i��޾�Ejd[�Ϯ���}�Q��wo��Z������v��&"p���i��;7�ݳ����m3�����3��5a*�#00�!(e̠�ր�6M��f�O��U~�V�1�**�����`�L�R^B��L�<3�
�aey8�-_�ogyX�Ǐ�_a��~�6�͇=V���gEE��"[�GVt���{�x�,��A3�%83���=��C��$'�np�y�'K��2�iY$��
�	R��ED�Y<��H��R���pS���VN�x�X,�/���,'�e��~�M�#�����1q#{D�?�rFy�C}��8�`��E��%���h����B�x)5!�g��>hc�~��`�r�� ��-k�`�H�^��rL�gU�S�*���a0C;�� ��Q�As� '��zϲ�pe,80���?3��*�;m��$b�S��"&��|�{��=־p�92ゾ���(Gdj������e�/)K'�Jk�� ��<Q�_�4�`���[�_����ͼ :-��
���?�^Ӄ{�(�b��QF�+g��K��&z3�	����T΄9�g¼䝑���e�⛩�IE�V�]P��T��j0 �� �%����u����h�.�����l �P�
�����[ a�P��w���K���$<��f�/�-8�ɨ�(�� WEV2��4c��͇�횬^@�2�P����^�U��p�V��;�s�Rآ��t 
,�|�2��g%�&z����ը^�do��8�3�MIcss�������fO�bӾ�D]՚Bʚ�Es`��`r��/��iί�T���Tivz���Nw��廩H��k5��G�t�V6�RM!�o���5x���V���� ��!��d����AX��o'~�oT�`��� �Ɗ�?���~^�u�PEo���^��^���g���/�B8��b���`������$�+{1��j�j@�	��������I\9�����?��u�|�<�~��bxhx(<��ڹr�X��~y�~ݺ���_8�f��X����T?�BՓ��w0����Ú��eH�-���tT�̪�m��a�:�U��_v�7o���M=�o���;�;�~Æ�#�a�yc1D�o�_���o~��U��w߆՞ܮG�xxg���A$v5�``��4.�<���D&��B�B�[�i��"E%���{�[*���0�fk�i�����fU�H�L��`�����}���3_�^��&����+��jE°Bz��Pa�D�坁�aL��c`>i,�Mk^�H�g�Ą���F���MH/ww;3oAm��­O� ���9Fk�[zYW3o���/#�/RF��l������c����	ٍ�zK�uY����P���Vߒb���.$^nd���:�{��}�Rn�fH��6�'���*?
�b�ۗA.��\��U�į#=	w�)w>5s�׉�@K��;4\��c��X��u�����r�L��
:�8.�xPn�	x4R]D�4h���E���֤f}gT�\����SE�m4~�H�^����S�8۽��kӓ�%"K`E|�����bg 1�qbc��}ӁB�؊63���z���\��)�q��|ڷ����hm>���9�c�ɺ����e�C��m�%�(��{]ڗ�k�ק�7C����+�u!k�(�NGJ��g�x�^@9�泰nBy��*�f�n¼w٤�b.�6XCn%`�ʧ+$�xʚ�e]��mU���I��z$���/�t�u�u�XN�)������3�f�ς�V��1����?�Z��m�����k��u�]]@}]JH�"�����']������쎥陇n!vW���c[f�� G�@��4!��K`�ale���Ο���A��>G�9#���8h�º������'��Wku�u���N�Z�!����X ������"6������2Q�_� b�g�@r���&��C0��s�0,{v�U�F�imRs�9c��t��"!<G8r�K�i�i��d-M��:#wV0\�vl�XuZp~��:C�L�y��崬�я�쩗)�R�'\<��%������?,n��!�%������|ް�%��Gr2D�L0:*�@�3O��2��r-o�gM����Sf���$� @+�]�ii�X�)X=��)w:��f���p	��#aB0�gb���k��;�N*.� H2I�G���mp� gɋ� e�B�'?n!��@�a�����x[D	�[I3�T��@[�#���H��"���2��1×ק�L4	(�1��|;+B&���#T'�������a��1+�r`�a{Q=,�yi'!1	
|JEԅ��e3.�:�T� �f�'p���_}@uoA�A;��x˳k���uvu��/` o��L��C���o&Vku.@�[�9��(�ZA?��u�76h���1��r<h/,c"'�6Ɛ�=���i�p =f��:�����eOi��Z5���G�i�2@2�0�P���'��ߖC���
����E(��l�zD.�YN�L���ЗZl������Sl:W"���x�wв<�<����vA�G���m;\�h-"^l����3c����`]�jd��:٥p��,l�5Gp9��|kۉ�g�q�oooY�8��1��Ôﵖ�ޗ�
KV����grb���R���扌��&���	O��;�v�*�/�:t�XwP���kjː���
�u%kv���g��,Y�,loJ/�9�~�BA��"�#���$��ף������6����m�2�[V�	�`�X����ڷ|����O/\�fٮ^� 0� l��n[V�=T7ؾf�DkNt[�>%ⓛ��|�Igs�ap��~ �G��~B���^�8�#oju����|ޡ��F�w��o�<�\�L�1(�\�J�h;a�0��cI��͡�ǆ<�b1�#(�A83����'<'�v1�0gP��4l�zD� mg�&����^�{Wr Vr8��Iz�������8g��m^+2=��Z���B�~����O����}��x��}:��+�=}Ǡ�j����P�������aiD\u�׮�m��ڸ<U~d�x��M�]l��%����5'}��7��ī�pQ�"��^_����kڶ3�ϙ�f��~%�3�
��N��C���z��T�E_�a��D	�U�9�ԗHsB����u �N��P�Gvrvb��Q#E���o�c4��,*	�u�oHnyxfɲ=�\��_�20��d�����K(7ѓY�Mp/��ܒ�]��n:zݝ߹�[T�.�����Љ��oߐ�&"���Pe~I_�]��B;�O�^�4��9�y��3G��I�������)��Ү|�ku�Z���bW1�}55]ȃ)�G0/.��n�9��R6]����z
�?�_�:uZ�VK��%uW���"��X$�>�}U�oD7��H7��1�I"�N�� �1��ZĩM���XL'����/�����"������7�46XA�����|[�M*x���/�D���Lu�ь.�u�F$+(���q$ٜ��U�&�ik��莆�����^ٻ�[�_�xh!<GXF6�G7����r����(4dGZ͒"��h@�q��.����΋��o]�aY��^�F��٤[�zv���{ۿc5	��й�h���M�����Fh4��ٱ�cD�tn����e�@aJ�p�H�U2���PǚGV��ATv 
��U�x�m�N�|^�H�OJH�X`����i���㯨�ע[�Tp�^WIwi����y�[QR��P�Aj�6@]�J�j}�̙5���Җ׫1�C��鰵\q�ڵK�c�$��9�z��1$k��S��Tο�b�&v��yyC�����@V�T���$��5�$��	r�ӟX�k��e���mf%E���=���6�����ĳu�{���� �d�z�;=��`��є��U��j�P���W����a웈{��8��@Ƒ���2�߀���Е��Ò�GN�8�;��B��#N��H� ��{(s#L�!@_����sYܪ��*;�Pt�+]���2ö�*j�]�U-k0�d���d;��X�k��}�?r��=����L��=��0��\��,�g �-����J8�?�~���[�=}G~`�W�@��H��@����V�t' �� f��ڱ���ɎlǮR�\@�d9�7�5At���えr�X����\���!��;�7�>5�GA�C����J�O�P��NQ��K�!�kW�w�	��5�^jY�S�Q�_%���v�#����E}Ē/~av��bf�LXH�����"���MTש�ӂ���$�|$�?��=��^�@�N$�w�ߓ���k�z�<>u�CW6?Iް�wS_� �xh���-v�Κ�V�lx�K�q��}_��@���o�o;�R��^���;�A�z�O���!B"��G�k�
O��DΣ+�>~���n�܋9+�G]g,u�X��,�T�K�8�8�~S�
i�P��:�%\�+������ZTuE�X뢪%���-)�VX���S�4?���jy@\  ݢ%�D
;�"ˣ0	��N3m���h�V�s��c%��v�]Ll�k}��"��� G�H�`�c�P�hl�G��d��v�gV���m02�X_Ƹg�&��d��-C����|KW���^���Z򊀪pؓi�ҧS�rD&�Zo[Pw�
��T�cWI��I�[�j��Gn�Ґv��M�A��.�  ���qH,e`��6gߚ��Z(����i?8�,M78�$�JA~�0TX�����s@�ܻl ��@߆�#�Գ$	��n�|Oi^9qp]Ų��3
�b�H��u��{{��С]�C9;099t�<�%��&xHC��]�u �#������x��X���SJ-�(^^(fyc�j5C1u����D+H�֖�y����4"�����*/"��-�k��>^�籒
�t�@I=�^]f�FZ��r�
o�^[R�-����AS����z�`����/Y�B�^چ�*���?��>��MʻPU<@Uf
-�M�G�Ҭ4ҽ�|��a"�t�t�t���(�����0Z�H�i������ك��P~�<� �[&�\���=�Z�L�V�1P��4s�h�ԅ�y�����[p:r�<Զ�㺟��ڸ;�t1���B��"8��.[�V,�n�J�k�K���#Y��ޢ����R�#�L��*�F�~�y7r%�ͮ.��u&YR��]���į���.)�NS�@� ���4W��%��P8�Xa7��}b��A �f�,��e�0 ��C2H�;�2��ٍ~�
���l��G�+fdXBcr���&㥵����Bo���."NW��3h�ڒ��ctq�CQa'k�%tR	��#W���gjW�.�����^O F���uTs<$���˃���!��dv�kגF]n\��CZv?��OL���{�ڵ}#�0�O=4Վ�x��7^��&�ܸo�����[��w�n,\]�(��J�XWl�9�I��]qް��^��B��?T����
;�qwI]ܽ��ށΗT��������]�����|t�(_�%�����p��j�0W��־���B��� J���w��C��bn�C
�?6�^��;�q�S2�ۍ*q���5� ?�n4�����4Z)��M��Q����O� �*:r:��7O��1��h�g����;�J�%Wi����B"�h�S5W ?����졔�N78�~_�i4:�>�a����;�MQ��� 
I��t�⦞��`1���m0���m{?<�����蒂^�c���4D�7��#�N׬i��8�4ѤZ�븱	�2�jljFqoEo�����W�+M�76�V63��t�v5���B���/d��Rs���*���WRao+7�T�ߊLI���(���Z&�#�"1�B��o��2s"�!�*�l(P1�7
��@�� R�0�X�;��"U>�H��\LыH�e�	O�`W!y�A#��w�֖I'��R6ш��@WZ��SUwj�ʀ��#₮wU�����B�
���KZ��kc���mr��[ٯ�.*gX��5��cW&�=;�?�
���z�@n�O�([#=��BG�Ѫ�,��� ��[G���m `�K�
��)�5=����qI�_�i,�;��+&@r��\�j���XWt���3wm�t.cX�4��'��Pm�AKrC�~3��>3#nHc��8Da,��'Gr�t����\��0��(0�P���E$��$���u��$�@Q�=x�K*��!�TԋK��Mb���EDS[�	U�WPZƯ��8��	�R���$�ќ�r�A�0W �x�t�jy�����Ype�IG~:�#[ޣ|��_[��i�7�?�+�ƉJ����nx�*¬I�yX�����?��)�`��X|�&�j��IY��p;4�F�N�^�[��D���Zػ�m[i]~U�P���c���
���x�a��h�ZMY�1֬\H�z�붕T�wg�����@v����Q���fj!TU�kS��.&�K=�A aN����`�.��F������a�.b��a`X�}�nr�=�u�*����􃡮������E�e|��]�f�~4@���[��5?����,���w6ێ7�z�T�Se��*�UVZ�ӯ=�=�=���y��Q{J��%�'�����T�O�9��wF{��e��z���(��J��/���5����Zw����?��]��fv�w�Q:�ٱ��	�Ց]ҡ��p�8��e������WS:����=��kh��Vv�[{v;��1 ����Y��a��RB���+���/:�jW辗h��}	xřhWs�\�s��=�it�F���aiF�%l,� ccƶ�l60w��`6�d�M�M���ŵ�|k��B6�}	�^��d����{�	x����gF�l�~a�j����꯿�c��Z� �@`�A�R���m	���)��o��r�@7��z�&���c���.�Y>��G�<�.E)U
�B��'�_�Fr��jp�0r�T]���'�Q�_�D��"/�6W��od��N^�}�b�?;ra���;�f-S~p�<�6���Z�f��π)+�p /����t�����ȳ�R�
�F�g���c,/D.`hC.5��'{p��<%
"�1V�%�T3����PSe᭘�R���kv=��a@� ̩�`8bE��'@�����3���,n�epg��8�Nr�ҺϬ��`dU�i��a/IW�����ɡ� >����k-��j��6�@N�������,�81�D�\ih���--N�+�7�J��r��$zމ���Tj�1ٗ��bk�#���TnoEơ�����غ������_�T�] �D�]�I�,o^3fOwG��(��b=C�c����_���⚱��#�[�q��S �d?�ψ�^غ��-X�Х�!TI��a�qBXJT��{��O��b�_~1� ��ȧ,&��	���%�7�mE�#GgWD� ƃ��� � a9�S F�e�f��l�t\�N���I��]���E�E�b�舑i�N����1R<�C�R"Xӕ$��� 0W�� �r��Y�P���f�sӞo�n����,�f����9V������9V���������z�����z[�𵹦͇Go�5m:���x��z�{���kY&�� �I���b���}-��-�W��.�we�=x�9�-Cv�w�{xS��;��?�ɡ�ǆG�����wM��q�?�w��s]�~���8S��)Im�wJ!>@yk�3f���}+��0�z�_�j�c�6��ɿ������t3�D��DH�$��D��h�b�2(�	c�!�+�a��[4���R&2�	ܑ-U{ZE	��}9^�@��Eʔ
��4���K95�ݖsi|A��� u���+�J�15���ܥ�zwK_DcV�E�{���!L���ܪNu��1���-��[�Q�ȥ���� �9�BW�V��3j�|$�H:�u �u��'tb�3�:��5��x]�gդ:��,�{~����,���ov;�ؠ�=�X!�D�-n��L��I|�N���P6�����D���)�0b����1�'�1�ȑ��5ء?sd�덛�֯]Yofi�J�Jt]���8"�Uk������`�-f��'J�ʔ��b:������5W�#@����b3=;'wx�@K(����Ww4o-&�z�֙9�m���zg�9���;V6�]��a⏂N�
�"� ̻�i��\0f8x/�+��l�]�ۺ:��{=r1r��Y��ߺag���'VMl����R����?
�\�^�Ƚ�[�A�wV
�֍�C�9l���g�!uo�@9!��`a�g�$<hbbf���N@��g�l�Q	>��{%�<�n�d+(Ļi�(���%xA�ub]�k�\�/��[�^y��4����jO[?�uz���-�����.����̓�H�2�ԭ��ӖЛ-��^=q�����1��E�P�f^��I[�Z����X~��u/CmW����+�2����3�ȕ���F�I�AC�b�#�@�(�DYQ'ʊ:qe��j6�Y4u��K�`)4TM0��l=�ΝŮ�p��k�[4%KA�PkRIعs]��X\b2���]
�KY���C�n����,���K�iT0Jf��B��F���-��^�'��3S�h�Qg8Cd��G39:UشI�]�,d�5�-�$���l@\��]
�� dΊ֨s�� 6C��!&GJ�aMIFf^(������HH�-6�����_�U2�(�*�{�O6&�U�G���5i�*'j�zyPg�._��W]�A��h��/�$�� b��&M������!�/PZo��[����ӏ��n�,nwB����jNt��B{s���AC#J���} ����icD�6'J���BȈ�?q���O2���>;���6K����g����ɱ?^"�A�O�t|S����M�N��>M��	���jb��]ho��daR�Xh.���F6�08����Yd
��Z���	��@��B��Q/�Q�a�#��7�r�T�%���A����_NN�o(x����.w� ���:wty����l���Z��ז������Ӳ"�k��y�Fs9t  �*_\^�ȷ@y�E�u��k��"Lm�+�L�=�z8;BY8|8<��6���=��c���w�`������oZ؁"'蓓p� ��#�Q��	1�$���ט�%L�������;6-�v&0*'G:��ϗ�X	%����t��x�.�:���j�_��˷ЌR&7a��GW�a��Ky��r�Y�:��Si�Y�C�~ͧ{�^�i?#/��،.JD�UX"�	�!%�(놜��8����9����N�΍wj)�(:��i@6��!�UhݱL��;�D��Z�J����P�F"�$��� ��z$91a�A�sb
�.U�"Z�V(ZCcDȱP
L4�&I�ʀ�)ٟ��� ���Z��H�*��^�����@���
*u�S�+!�������/A�\�fy���*�ve�+��D�lw�p��>z^��zDM�#jr�z���p�q���}�e�+FT���L5h�6�qe�&M(��A�[�X�s�)�$�%[��xR�w�,.^6�(6[IR�t����J�у�/�k��kF;�?x-闶��������r_����O�A�$Ј��.��[��ף@�C��p��x5VM����d���~>�R�� ̃��G�+� �>�g�}��?���Dt`������7|^�_����J�d�P|j!|���j��:Z���E�p5�aU�؈�^	��%R��FT��q����R�U����D�,��F���*�n�:H�,�ñ��MK�_�����
�t��>&Y��aq�r�k��U�?�6���Z�Z��+)H�$:Y�`W��A��B���|�O�=/+A������˯�@hU@�ZA]C)����= �a�8A�1
����6�^:����'i�k����y��N�]qJI�X�]��ػ�1nwGsy���5CŶ/'A}�D��`.lOޜ$W�O-�X���Ƴ]]� �̤���*VI�������<z����Z�~�>$�lI�$$UZx��/P�Yb3z�?7m��d�Iq�B��e�X�'s͔?�4������WH�YJc��=�*e�O�~�x��$H*���<z�O$�GRi�٭.�i�QW�3��Rya��u�Q�TA��5�J%D::lF�ȭR�T�I����y�A�����J%7�̓���1��]��Q��a:�M��T>E�R��ht&�v/5+Ft�<����Y��㰿�7t�oN�����z?E�)x�q��a�_)�1��.1F�������I�6<��;�>{hc[r��*���xá�:�B�׶O��ۘ��7m�3�dW���Z��ԇb�dW<���pĝ��8F���2��Sm��#�`ªa���@���p�x��Կ�"#=�\�'V�|�?cۥ�m<��L��)��˟|�$�cO�`O� �[ܲTb�r�\�$�ɧPt�3���:��Y��8��h�̺���V�5�L0ԟ��G}�?�*�����F����q�TJ����k��Z^I�y�zQ&8s+c#�	1�fh�Xǚ�����f�Ǔ�'�{kk��4�y��t����+�f��㥤<�dI�wQM�K���s�L@+�1i%i�}�}�K��4&�a�J�ɬ\�F�|�C���J.���&�^�Z}�>46;��x���*���}�-[�\�
(y�Y��: � �,d�8��5�&�W�s�g�MIE�3�d�P��zN�u#au2G�+�gԙ'J�Z��uU�>[�"$�6o���[;z��ٽݛ�&�rƨ��@4uj�;S�ov��c7t�ώ%�a�b4%S�*��6���;D3:�s��=D��۰V
���9x��k��axD�U��xQ�5��wFyԺW��9S)�Uq��{��GJ�:ٜ
��=\��X�GKֽ����涬��M���1H��G����pW�ǲ
�?ѐ�=������+�MAIv[dEܬҩv�M�V2��G�7���C�h�a$^�9��jl}��	�yL��xدx�~����X|�sV�����2g�%c���R���X)n����x�U{�U�����l�z$�IZF����Sk5��eZ���=���i��0��4�����Vϒ�#�j�:]�rD=���ou9�-ىf�B���<K��CPZ�<{"�G��I��Tu���Z�'3�]�YfVr��զb�=��J�ۦVBA����yH�9�(����B�$�L�P���m�3���LZ��Q�]+���`�U9H�[!I�c�i�,�f�+89N����l�4�����x���|ɖ�_���_G�2\��������&�Mv��ק|�T���ΤU���$�u&�v��� ��50k�Xn~+�f��"˾��ª��*P�IԿA��'vcL� #�Lu�H�9�~��FV{�{�{"7���L�f+X�z5������-���39�����-\�
��(�Css������h�M��ިLg7�:y���S![ `�lj(��:�ik�h��򤲴MZ���T6��T��"_��J��	�|�/��S�\d&h�NK �W`�h#��J5=j�� ���GD5�����l�-���}�a7є�dJx2�VBy~�� %����D�"�
�dm��f�	�HM�g��Q� 3��$����[�㱱�
c�Edx����b�!]hE*�"jD��5ԇ��u��]�{Ɠ��]��@���4���7�6��-���S�m�u�`�g�MX�2&�>��i�8��}%
u.�*QfA��v�գP���+��T��ڴ�G-2Z3�7n���Q��h4؈��������2�/0(����ĞE����hz�.%�Q���X��ǹY�vB�]��=���L�i�l����B"M�=[�~�N��σ7���(T:�sz�Z޲����g�õ�g�U+gd��u�����<Q��Vȴ(�Z�*X�����_ r`�ioқT������PǏ���~���-Ǆf�#��ʓ��afom�Ǎ��>�C�#%!5{�����g��Cg(/x����c!N��q�3��Y���H�>h��Z��mOy�2��Ӭ+���w�b��x�����#3Ӟ\����͉�:�J�S[L����:��X���HG¬TkX��f4�&fw���K��z�9Nd���D�9�N��9fS3�I<.��[8������ɳ�9V��ձ�a�<�@��;)�
+OKu�E�R��g�Ykv�t[V��T*��L�,?[��{�����1$ř�*��ް	��nq;�`h��kh��h����$���+�
�B�(�شe��\E��.�$R����jT�.Iː]�pe^d�"�z������>�`�A��h�dٜ���mEU�`�	�e����}���%���!Bn�s���#�>�:<0g�)|pm]�Wɽ>��>��%��E��v+҉+�#+�K>�r�FY�R ��ņ�ct���E�5��΀��^b%�4��z�0I=@*8cDe�t��V�"*��j^�`H<��8.W�(8�$����<z�[�_���`N��up2y�Ϩo7*�+V��>��[��+��#:형f&$����ĩ#�<�RU���j�K/�t�����:IRN�I)>��gR����RQ��ROӔ��-N^N�J������L6����$o
^ �J���6���DhZNU�Z����7����A�^���݄��V�GXc��VBO�ȭ'	�rt��Q�)����>�S��4Q��%���Y����dk��K����Ĳ�H4���;bٖh��5r��	ecі�h$+^�g�[1Z�7�I�Z���
��U��[�7"�og�U^�4�,o%�i;���o�om��Z[c�X.�gs�.��x,��f�k�m������"�DT�q?3'SR(R��s��;���8�����%O`\r*/?K�}��'�ش1�.�f<�Ԓ��.3�P2�O�Z����z��ً��Ǥ��	t�#��m��*�2Z�.e����I���u��H��;� ��Z�������U���ĥ��";p����EO�V�R�N�6�^���݄_��x���9�W��͓g^��6L�P�Tz���U�G?��iԅ�����j�S�&k���RdB�L  |�`���v��T�Y���Xcn_̮��>V#'/�ʧɿ���|~���
;i�T����]Q�CE�?�`���B�:��?����aԆ��*����~I��*z�v�/N\��,�$Q�
t{qBꇪL�~wA8���(��j�<�pڢ�Q�d�%ԪE%P/���Z\�tq�� XZ݇�^�������yP~g��yJ����".���A��E�!�W~�����f�F\"R��	��W��!��핸-�׃�!3n#x	�h�h�SKx�]���`CM�Ph�A�c\����'�y�|�$~e����S�/[�5n�\�X5�p���+?����~���o?��5�}��vA���}P�qd*�&-I�7i���<9{Ri#F����J�`)�+>��N������)��T^>�+HQ�͋�� �p�ܻ���{a��%���|J�+i��|H.����O�"c +/%#��\+�pr6�� �_�m6����W*R�8�Fe�8eهjC؈u� l�0�Ŋ^�}��Ƽp �a��d_e^`�	���&z�/�+I6�""L�%��n��l8mv��Y$�">G7�L^���z{Ɖ.ɹ��B�;׈S��EU>^}o"O68��ϗ��<�_SR���Vi���1*5��;���U���G;�N
��zZ �����<�	�gT}����W�9�j���:6<����ٽǧ�.<���T�.�_��;Oo�OI�IS̺����C�ߨ�T���U)&e���#�~���'C̪��I�d�w}s��߾c���Ep��A�ߊind�?0>bLЩ^&Z�I�ar�2�*�8��C%*Wv;�s�pT�:"�ҫq�O!V���ݳ�����D�}�Δ�it�\	�c�����s���Ʈ�&,����V��rH��V��{l^�5�ow��kg�]��;��Y�k+ߣD.g�����ȣ�>�?4)\�?�����l6g6�{ds׭;�僑�;��=:�.c1�5��Ҷ!����[>���޼���>x�3���#��U� L�&*m�
�2l(� E� ��(����ͨ�X���eB���&��sJZ��g��|^*-!.�gL���Z�_��7A��$�P
[���Po��O��O���+�pe�7z��7p���f�{��<gw���yR�W)�N�os},T�Yf]γ���X�$�dUn�.�f�	@9D=��}����A����A�d4h4�6���������T�ʡjq(��'�E[�T������bH>AH��b�?!@��}@vU�/�����{��Q��L���xF�`�8F�0�YQ]�Q���
�:�[l� k?�F��r�`s�R�mpB�N�p"�	���?@@S�r�`Wk�IO�j��ڒ!W�7��TS.����o|���nx�?{�I�����F������6�<��V>'�k��/�y��/��=�����K�}���K��ܸ"�����GK={��R�\����vN����Pm*��b��,�!lă ������!͛���SrRyqu��^¼�����Y�k�����]�jjz-������4��zU6�{Qe��ϩ�(�ĺ�%�Rjk�e�[8�����+�͟<�\]Ca>����W��>��YQ��T�>y�A����U6=A�m*:��|_5���G��P�&�TmU9��ӑ��Q	���p��v�Wu�N]JG�\E��E���� ��o]�ۅ�Q�{���U����aN����B��6r��:�ӑ�8(a�J�C�z˾�����r��^���@��0�A��a�ۘZ^9�_��m"�I�ݼ����F���O;�$X����7U�����?��_M嶰�|��V}:��}��v�~	�;1���-*�s�o��(��f����ʤ7i�?H�۟W���yǔ:#�����W�5h���y8�,#�/i}����7nJ�׀��;��t8�N\�@W���(W����S�:\&\=��sv��%P��X���S�%�K�F�kԼN�(E�!D�z0"�������?��1�?e����Vd5�GX3T���}�T�Ū=d�I3��'���L�A�����g>�z៪:��r:ac��T��[�����V������wz� v�dv���=w�p"@�v���w}78rIjٰ����?z`݅gH������1�~�����;N�ξpϰ�_���O�y���=Sm��5u��tn;<0z�umu7��Xk��<�����(i{�x�I�g+�6B4BpRg��o��i�����*�6�Pi#��g���2R���qW��+K��V�;$߮e��ȣ�R�濦�=�>s#*�c������j:V�ߠ�)¿-V��+�� �a��\���ķg��cׁ�bz��w�$y�R�g�����W��@]�o׉�A�[E��"G4����+	�֛�({{��M�[�j~������ihN%�#6�h͢�4�.'�C��Dw�)�[螹��Jjs5��j�L�}؇0��榕|Go���y��[���Do���ݶ��о�ӽ�ͺ��z���s:g�^AB>֤7&�ny`[{����[W��F�
ޮ�W�p��M�����/���_�*x�'`"�'�EI�N��M��'����kPO['�KN��-(u�J"^>�ҜNc(�Ug��j~p�1�z�iGq���ѷ�l.�ϡO����\(9��%~Dގ{�AUOS��,�?�N*[I�@�ݔ���c��V��C�ٰ��1�%;��u��^����U��M���Gq������6��^���|{$U]׺��ش������[��}�P[���<|���/�3[u�Xa�@�&Q$���kn�sCr���A.�3Z�s�}k"���{ۊ��w� ��pF��&��z)��m�V"N��bsMM����
؈.����<�ɫ[���ن�J�c#5!�HI��*E���9�pCۿ��nt��%t33�(�8��O,�#3׺f�� ^�n!rO��Z�vf���H���e���z���n�ml�ƕ7�sun+\��Hy3�ll����͎쁎��:���'����.���[�H�5fl�mW[v�-�;�T�k�����[��!1����{A�JD�Cz����g�-��9O��6�D*	�p��9���b �����߂n�cPR�:�>��E�ŵ��t���n�A�T�ץ�m*�≾Q�}-�,uR)<��1������_�Q?p�ۇ^��4��o\�������	��S7�z��kW�3}����tG!ֱ�7�n�����_��o���plhGg��b���:@�����;���W_x2���@��O��h�W�"�k-?F��኏��N�6���c����FJ����L1�x��1r7o�����bQUm'��KZ�}I KJ	�)��}l�w�T!���vFN�1gQ�Ps1��;�f�4����[�<�z���QO;�Ͽ?X�v�X@���T����g�|�ԯ�L(H�s�{��躹3/n�t��ѹ��W!��bT�Y��&]y��˫�?l�K$2:���,l����0���b[���B��[��"d-�Z��q98Ut�sb��0���\2�%�V�2��a��t�ń��,:KáX����z�}�;g��#���$Z�����bv�Սz%
�be����l�%�����C;�߱��a"��7���6�ۼ2��{���/�����{�������4�fF�iI#�:-�:,��%���|� �L��@���p��$dG1/d	ɾ�n��������������F�!�m����ju��U�������]����]�L=��z�5u���Ѧ�`���C&��k�V��'kF��i�~��jw��ޮ���KK���S�Y�)�`���֑),�8Hl	�9����#m��X��m�O��6/�IdBg��߼��g�?c:���]P�GTk@�+|_q��ս���J���oK�f����%���vS���wf8�R���ˊ���;b�eU{>~&�rm������DP:��U�ʯ9vM���=Q\J��1V65�`ahg�J{64W���}5�%߂a����N�-�v{V67l\R�B��g�`|.S�{]C��1m����µS�Q����S�f�'䑋�<��������#^	���N�Kgv@~�f�
��. ��/��#�4��ʬ����TR �<�g��@�ZB�=�ږx����"t!>��!A((N=?(Z���5]Ȃ�Ѕ,��0����y�Bū�^P.��~o���n��'.��]�l��}Y)@E���������������P{��a����TtQo���av����ǟ��'�Bcv�Y0��ܩ���z��H��|J��+9l�+������ŭ���`����[��1}Z�@�B�*��J~C6��V1�2_�O�aq�O�0�;1д�/��+}F�2��L=���
1��Z�'��V:����s��4�9�q�_�����#��F��Ë*V�a��_eAS-#LY�fκB(��4�*˒.E"jS��j�|f�c7}cG]���6m���'�`�ڎ���a�4���Z� ���0��O��<�s?�!.����{��]��6�pfϑ�햎�[��(�1@�[>�	[��@+����㭍*%�k�u�����ȡ"�Y��R Q̒�3�h��z;�w;;j!��]~�U{a>(OSQR�g���V�^�L��%��a�E��jB5����b�B
�7�L��0���m"�R��W%ͫ0v-�,67�ք����.����5�[�dE�h�2�x: 1��0�V���U�hu��?nmu�[>zǆ��Z�YV3y�k�`�N������!��/v6����Ӂ���(�M2�%����{r�g
�9�c_�K�wd*��I-���f�Y�C�u��(J�v���?8��.�|سj�?!u�����ƴ�9
�X�?���n𨱅,�J�� �ɑ���т�]��޹���:J��������p�h�F֔/�qU�:G0�V$�c��N>N�Ri3�Y哔�����,��Uy**<E$&L��2�m�Ts�֧Kuؔ���(R��C"�����/;����E����s[+"狒�B��<��\���	��[Nc��"j���(^�x}��'\�jOF=��;���7xqg��$�U��h�e�&����hҒl""��`)W�NY���>�)RF���9�t,�?��w�qKRF'9��.�VCv�[1�r�0񃩬�qƚ��.��4�-�����xշ��Ǭ����`�=Nf���օ!�y��]¢" �^�n�e~g����יl��uٵB�=�u+������V�BjX��w a˨� I{��P]#˺Erye���|R����ʶ�#y�����Ն��h�]����K�v!��&'�}�.;]~�9�x�����y��j�m�s(CN�
�;+$���+���/)T^����{]>\�[C.;,Q���#���7��h5�I�Z�"@W���.%J� ?U/�U�H�R�P{k��1M�����S!��+�0C�'�u��UbLw��啫/$:�E,W��.�����(�}��]����:��s��Bu�"��0�X!��G�SKs�m&mo�[<�fr$j^ݒZZ,Y��vw���R�"=Z�H��E�H��	� �4u�X��065�[2l[ �$�QYt�G��߾z��+阬�}S�dtzf>��uhټ��|��C�6WW/�ڝ��/�[�U�����K�`,�[魯P̤9�f��`�;��'fdyu&�ne�ByQ%�^Uҋ��l��@�;Y�Y��ɂޕ�w�����	�W�f5�̙3��u����f@�J���x��h����eI�PŲU���
G��*d��\��.4rˊ��_�30ҵuI��~bj�Ug�Hܩ��{�6Mt��W��̈$C�Sgv[-����\�L���������Ǩ9 �������#�-�d���P��ۦ���C�,��L�2���Z?�����i�<��t�d�r7ϔA����$Ğ�5�a��Y�\�Y��9QV6�~I�:(+�J��	 g�s<�j�]��==�������y�$�%OPd̎�_�_� �Y�Q��R�z����V��e�/`���eѶ38w�����F-���h6Z}��}9�n5��}8���<0�4���C>�H���d�*����Ih&uba�wsr)'IG!��u[��.��)���?@��Ө�/��0lJ�^f���E��rS۩�_Z�hmr���������/n�z�Y���cu���@c��E.����m���Y��Z�dj��#�MN�������C-���J+V�肔�/V�į>���i�aaY,�]�B�8;#3��jM�]X�	+8ir�0��#2�ut�RHl5�قU�p�EH]��[�RB�%��㎊��Z������؋?g0�����T�ogw�ӴnɁϐ�������mx�pw�Ƿn;}pRW��~�䀷|š%]�WW?�Ê�#��q+�Y���} ����ROp'}���*(����gx[�e6܍�J�E>�3��hUm��)��B&A�0������(!����lw������x��4Ӟ�7�:�zus�/ev��hzi�X k��Õ}�uM��Ε��:SWN��i�[Z�oj<�̾z���Kۀ������}��t���>@%r�?H��*%g�3��Xl��b����� 7�G�<�#��b�9N��&'�e�Z�-���ɨUU�4k3:@1��A��9�c�1zR��:�r���=�2Wqwm�m$ ���u�x��!�G������D�>��y��훎]�_S��'��s�P�����N�*�S��9,���j��]�y�_�e�X�O�_ұ|C���Q�"6'ɐ�̝f��^���G�'j�>�~�]#�$==u����q��2kZ�:^b	<�XY�Ax�%��V��F�R�D])�9������ƺ�t��w]��J8K�_�lشp�ّ�r��1H�r�yz�z�[���67'lUU�������@N`� W��Ds�������k�2����/�0��7΋����mNT]�*=l��J�I��r�K���yaZ=s��I(`��_R;���s5���A%�������e�{���C�:8�^ch;�Ԏ�O�c�[5���e�<�#��^֞ⵟ+Y~xy��5u̥2�5]���e�GV�� rBz� ��Ĳ�k�p����XL��%x�+ <ǅ(�ĩ�Ž�Ki��,�m�V�^��kU���.���dQ���:��J�z>>�"�Ea��L�l��DY#Z���Ëz����мwe�G��ڎ�rV/
&��$J������M��[W���g��:%��s�(�nOA{d��*�it�έK��Q6=+G�����=�㿚�s����w6\��^]�9:���O�}'��#w�/bc�j3�����c��@�|��Z�f����i�a����t�����]E�"��Axx���4cTU��y'�N�XQ��b���A�غ�9�X���9%І�L��R���Բ�t��i{U����-s���1:K��<fi7�9V�D�aR/ܮ�H2x��:��is�9Jǐ:[Cq��,fI[e�9$�Aꤠ�q&w�k��j7�������#����Ϊ��d\�}��1XL�]��r��s�A�!�,wU�nYQl� /�E�V��r=����6��(w��;�ae���X�2�_<����N�
��+�tU��J ��bߧ�v�lUZT�$Y��[��*͵�>w:4���~TUYQ8�s���m!U}$�k<pv?3m�-�çvUq4M�%���-,N�\d��Cz���h���B�h��V5���a�3G:����;ݸ��>8[��&|���]߲�q���ި��s�N�޲��C#<�G��%7l4�vv�N�2�a(��t�ھ�7�7��Oh�g$)�����4���3��̌j2�b�rֆ0���_�Uko��d��tff�n�t�/�RK0"�q�+�y���ɚ�Cm���5��Mk�L�Y<��l���A+/�{*���I����h&��,u���%趺D���C	?���R��x`Y�޳7�m_����7�4۱���差(�6m��=��r�ܿ�]ә�\ucߺ�w��0���tl43|��� �"���ʽ^Vlm��I�L�$%��L��?�f�i|�)��-��#r!��S�YFR\(FĪ-j0�7�����R&Z�����uz�0��j�X���f��ߢWa6,��ܤt��W�,�mX��4]�A�0��ۯ���ؖ|�
���I��#�D\o{�a���:�~������u���9!��A2ЌA4��6�p�;&�<�LB�����OR��k˶L\��FX{��`�10X�-"�4|�qC�Y|���Ȋ���@���n��E��C8��ShgY{���Y�Rs�"f`Ҽ��Q�[��yG��ur�3
vR<���N�ט�"�o�`���g���4qЇG�S��27����.�F-N�h�p�f�q9#v�nE*�|M��Q�#�r���N��^��"�G��e��c�i���v��f���5��U~}>˘����\,^N����p�8��ߓ�@1���@(	��KѠ� L��`p%e�F�P��b�����O�^�%{08��!��ك���υ�mM7.J��[:ҩ6�r�;����^@o7�7#w�w��0�C{���U#'Y����#��U�n�8%��ST�aw@d� }���5=����(\�ŝy��kL��_�+�.������t�ߊ�-�]�a� D�;ɟ�O�s�!Ǳ��>�w��	l%S~�H@� �L��P��:��d)�1��Fs��DJs�$��������>yl���{�:z	���͹G�?�w �������I�ʝF�������&�%0s���&�Óp.��ܯU7IE$��}���4n�:%��@V�x����@}��v�@�S?΍��������	FO�{��o����?�l=�0$�	p~����0��*�*)��$535���#�0� y��_q�L2|�Σv�P%UV̫B����S3PE,.��5��U�VQ���<��X��p�x������Ҽhx�o���80Z�:�[
�{Ӭ�:	(Z�X��!��\�;�y�IV����4�w���i�*=����E}�i��▤�H�ā�ٽf���#�o=�t�;��D�SG/{��+V�|�;�h��i�[�Fw��L������	p-ܘ]���<p���|$~�^�R��n����:{(��[]�������'�|������G�&)0��<u�ћg)�"��!�7���ߡ��`o��:�K��|>�.���m:� �vg�=�s���9��u��F|���03v��;����>��YI!y˜���甶҅π�
Ƹzv�����w*��J���'�;�9q��yEx���W/H�����'��0pD���O]���\t��C7��S�G��T����ݹ4�~�w��(a�������;���|x��3�6�;2��z�
1�!�PQ��!\��ӄ�&�Z�r�3D���K�h�}��ߜ̢_A%q�!*���aTx��mI0�-`�6�C��dx�S�l��s�3y�;���.:E��&pȯ!&L��t�o#�KY�2��ty��j���N�@�{�Ͱ5�L2�B�4^�4���eK���S"� ��)ԅ�j}��x�B���jC+�ρ�j>�BaW�C���h��^�5�&=Ś���c���(]R�xmw	��@���b��u-�7M�]�w�^ J�f����}[�ia�Y���-X�I�E��I�B$�(���^1�qO�X���@.G����V�|����8����&�4��f�4X5Ӹ#�-N͆B���i��4=�ą�gj� �S�T��Ө��ݘ�f��4|X��j�X:�Vޘ_Z��9�?<�M1���
z�|$����ook�9Rc�H�e���mm-�,���o0��7��[6v�*�+맺�8�����oi�u<h��k�:�>4pǆE���m>h�d���P���Ѧ�Np�,N�	7�Uź���X�ܲYMւ�=�lw{���A�n�>4�QeT!�R�$K���4��,�(,9M�g��H���q�)a%��Z��eaѩ�9�Ö��N�P�-Ogզ���\$^x��~n5j%�D(b�P�2��Żޢ�4�KF����ާ���?\�3��,�6�$��P��:E	ҽ	����x������~tg�,�(�sv�|�r�kC׆ή ���g���W!�ri����>vm�d�wylm�)G�Ɓ��^�"t�RVE�-/A��ѡ�/nk��tߨz��	�R10K��9F�2f�'��sX��DL�ƭ^�}N;�*G���Eʀ&l3���]�����FO>�pFݥ:�0���iJ���w��E/��<�R�H.�%. H���g�� 񣃬��Hu�W���)gH7�N��V9M�;��i���D|�P���J��|8��,h�T. �D^���(X��i��@�+4@��d3�H�l�����5�,)3�<Ksr��Φ��Ǌ��w��`_�M�����@4�=WP����%ٖ굛T�ñ� ��4հ������
�2�}}���&6��E�
a_�P�l @w��?5���]U
��g����i������m�����;F��z�4�ʡm�[�]J��= �cx�_�@e�dO��HZg�[��u��	 |������7�޳����MV�-���C���Uc�ʌU�:��! {f�,�%�)q�Þ�b`3Ă�,G�FŽU�gWq��=.8Q�N��OA4S,wW�=�N�Oe�����D=�7V�^G]�.���փ�P�@�,����Cxn��e��[}.����������Po=@��.G�j�z��LJ|�I�^�z&- �4�iP�Z��<���������D�c�n���PQ�T=�������|ӫw}���M?9��k�u���\c��� ��~��E��nN���"����g-
���̠��P�kb�Z%�2���HuZ�،�o���`3 ���?�-v����:�^Q��䚣a��E�h���c�DG�t`W�*�)��&�e�5���t�̤�A���i5�R�vu��"�f�P��<>p���R���dqN����n5ٌ�IƟ--�ړ���eM	b��!V�MV.�a0�j�5�(��$��.�e�>���v�닷��C��wȥ=V�U4
>��xɵ���m��"Շ� a�g4,���2Y� ����:�e~2�e�*�} !�������\�_��
�_��^�UjҘ���-+����7�_���ي���%ޒ.mK��O�P�w�@�Wٓ\��%��;�&���N�ӕn���RN��JN�*i��cW�E���M0�}k�u��l�5ɑt�e���ُț�V���r[I�<�Ϟ,�i,=�?�1�ET2(\p-�A;�/G*y � z�\��5Վ����/#��!��,�����e蟗+,��������P�g�*�NL�A"� �	���k&���uH��D�&NI�~�Np��~q���K�^�:t�f��8 l��(�+x�2�D�Ŭ��.x�*�E},z-��8��m벆B16ql�ϏǾ��j�OK�ʁꦁ�HH^�gi�iվ����=K��x���]�j��?�Ɇ��`7�� X
[��m��D6�"M���1�O*&@�41PI�d°E�˂6�����kוR[��Jm�4�3��Ҽ��X���ߊ6�Y=��M�Kr�$�0Ⱥy.��S�����f�]��D�I�0%�`Bfg���SU��`ȟ��68�|
�y�|��sU7�!��R��5���:S�ħ[�)�:��թ�׬�|����~�.��04���W��}��F[n��=�O��`�u-V�u��qX��@L�"���^� �\��f7����b�ʺ�0���H�8�4�7E��iz��:_8�V8,�-�CЙ�v��rXە���C߻��=5��;|��/��=��;�߹dd� q�������]���\���2������۾�C�j��xl��"fX��x� �gu�shM�6�����ML&�j?Ɠ�]B&�&qX�P�� �6b4�:1�]���ŚZ�����6��R��Z��d�)��!6��f��٫��Oa8�:C�f8�ptc����[ә��g�	��om\u�ʔ�qӖsD�ݒ����l���F�[q�ީD��.*���f��&� �\�����=O�x���j��>@�<ݡ�
~;��;�Hw�#�C@���e�iu^������������jw|gG���ZQO�F_ѿ�]3���t�msF���r��{-�#ۚ'n�7���n__o�LF�O��2��YʌVC�I(��\�v�,#���]@c��	�l�b3���h+B�u��f����'d�7 B��5�,��Pt>�g�Z_��*B}�儲J��l^�_��s��Whk0���M�X,�r2�?���s�2�z'�^���q�ğ�>2��S�x���vV�K�<:uq^V@�@+�����f�wM�+���[a�'k V"r���%���+e9��H@�OP�=����]$���d��@��`$,9�aA�4��#0T�ȌJ��
W�?p�,v+(\��¢��u�ί̯m�&�p�5�.�K0�S2�i(M�/��<ut���%٧� קL�Ģޒ�M��ymg�pC������ӓ#�]|��Et}|�K{����w>����G�"������@ �S��B$��#^<���n<��#N�Ё���) [ia�R�c��XL��SIS�k�T��ԲZ�i�L>����w^�Շ̨d�'�;EXxY@�����+PI)�xH�E(�4�Ƅi\�4�v�2O�/$���~|�K��Z��BM���|G^���Cs���9ń%@EQ8���绡	K�`!>�
�c�
O��Vx�@��!�3�w���(eHL,�9���H�Y�0�+$�a='���i���:uc�r��{�w����#k%OeE�dW�JR�wԏm�W��-������!�䳙e�d��������ۃ63�H�B��w(|o�	=���)K!�"j�Bj�N�2�>����Je��I!,�5�+��V�tÞnu; F�<��2u ^~��I]�&u'��t[���3���I��h[��#���;��@��HhU�wN��k��d�r�8O���z����[P-,u��2��>�����Uۼ~2�y�_�U�f���Xu�qD���$X)�e�U~����x�:��
����k��aK�E�x����Ѝ�|8�;^(���ޗ��U���{��W�bɾ�ly�m�v���I���,ɶYr$��@a�J�>�2Ӆa`�4	�ť�f�R��nCg��´�6-m�(�?��+�KB�׾�{o�?��9�,���{u�9^3�5�^�%)��%b���ƾ�@|i��	r�^��� }���c�.���,2{��;dQd�+���*��ē�!�!�����X\W{��aH	�s��ʞ��;g������ы葥���;��jV#A���/H��Յ��B��zs��tc����ZXEM�R��fDϕD�Z���s���-�r�Yf�'�#K��ދ��f��s��@��/��|���ud|I7�ڇK�|I)s�9-yJ|�5�V:$��_�J��%FT�g;���a��4{�)|�Itȳ�Eϳ�֜�lL�(�<�K�����2�+}��+��_��w�}�Q�[��4��V�{�_���ӛ'?rh�G�[�&?K�����������"\���!�p�����0��[�����J��'7r�/�Ƈc�R�pɥ��Ρ=v�^�����Y��H��d׈�d
	رBƤGd��ܨQJ����{h?�M�$��%?���w�w.1[��
�+��gEב�w��6�[M���\5<�
$�c|����^��3��f*Uz�D$�(?�o/Vv����pp�&I���均:�4�=C������B�V0k1�U����j�ն�,&���Z
v��k�Q��r�7�O������|��/ti��J��K��K�EZ��_]J������<�|�
��BI�3݋�/�
�6�8W�y�'�[+�ǨB�����Yw�3��E���Y�[��Jo޴ڙ7e���yr)r�̾������M��R�����bx�V?X7��C˔����m�%��n�<1"���u��q�ݵc{y_��ܼ��S��2��j�8&}�&W-�J��Mj�V_��j��4�Bm5i�U�a����K/�1���UO�臄{���$��އ]���RO�l��X^�U���~���jͼ��F �|���HdR��-�;���y�6�S�ͷ��ǅ30>.�tv�II?*�A�L!͔s��<��&s�1/o7�w���w�nB�^��2�n�:�s/_�D�N�f)Zd��V�|uMkK[��V��:�N�x=zCI���k�z�]-b���[�ZD>-�8z���[���ɀ-��*�n/`wƮAx��(~���<~��S:����^�"�Y��_i����MM+^V/�W<��"�΢��`Ҳys+èmF�E+��K�_������A!�?�z��hP7���c���4_�a��y�.��*T�v�~\wc�����fu�ѵϼ�祐�t7J<�cp�r�b"�������{�<��x�n*�4�Y#�Q(��ۏ�����kd��M�j�ӂ6�h�=�h.l��_x���� x�f�S�RbW���Fɱ~���ߎ��|O)�o����=��b�	�Bcf�v�D�!b�YX�!)Lz(W��4CӠ �K�Q� ~6Q�/��#�K� 7-�b���/�QS�@7݄x����{Ȇ���T5�A���.�s��C�̄�:�b�Ju[��P��+n,s�в6������-�Wm:D���F���Qg6��y|��2?kD.Go2�&����[����^3��u��^A�-��S]���%�-%��%-"t��]�nl�`��{�*��t:SQ����"mz�W/�Oj�sG��]o��V�KO݃���bB�C�
�����?Q\t.޴�y��8�o�|p�����T'U(��ʶJO}��P�Q�E�$�Qulm��j�pI���i�DY���m�T`�
��+,��lmp)�z��(0��Z���[K�ڤ�U�@���5��j�V�S˕F��^�^��W��bG9�K�t�M��y/����]��7v,eE>�� *��\��ux0�W�2}�1ϗ��/oW����)�2����M��"��cs�ٕ۔�_0_�ڒ�y=SD���wb-VIO�UH萲L�J�e^@s�f�Z&"q�<���%��1��J�|Is��u,|I�bq��/11ǘv�	Jl��b�	j���x%�t��*_WKm�:�j'��:DMR	j����0>2�k�����g��i�pIX>8���zŽl]��!vC:<����;N��9�^esnM���r������xSܱ��«��-���i��ҧ���_������}u���;1^�j�֞Փ-�>=g����Qß����/ïˋN��sQ���S�����F����e��W_�YV�KW�/�'z����������@}	Je6������ 3�>�;PsK���/�5��%t}CC=�Ut1s����a���G�R�|'�2�G!��v=|�O�k�B�#uu�W�� �j�݆�$���Y�%��p
��>�y�>�K��O���3_a���
PS��)��v�jv���^TP_P_�^6,1���X����AR��s��c������z���6��c��iy�rL���{��/����š�h�Ӂ����X�#`���#�;n:h8x��t%�Ъ�cW[�H�{6��T[�f�
�Z��s�eV�>�С�{c��=�bW��X�tp��ݷ+4�L��^|�ًy����,s��	!O�p�K8/a�N������e�$�	����7E�����O��{���p����/��/!�,_�s�����E��Ő���bY9!�q����೑��l>�R������Z��]�<��D���wAH����lyg�eW\�vP2����ni4�1R���U�P{�V�N.���L�9�R�~�Z���vV)��'%r��\�Q+4gD
�f���tA�A|�Ɂ�D_I���D�N������"1��<Nh=�$�V79m�Y�;NB��OSr3T��	1>C�z��Y���1h���-G����gi+ʮ���車�^��L���B<Y[+t6#WT�d~�S(t��~�lӠ7���6��!Z>)R����Q�T)ՋO�+Y���jf�!{�*��sdY�[U�&ԨZ!�2wv��pP�"�7$���fs�R��O���i��h	�d0ٴ�̮�o0ohYC�ѩh��H��0?�)�#VJ�G曔H�T!UE5�ݕO9(o�)z����;)3UBK�������//]�!���d���{�{~Y��x~�r���4ѕ.�P��� ��䚛c�j�	�R���,�c��{0��}F��m���ݡ]<��i�v����%MA�g�!�ܡ�J�ʧ�VE'J:�^��hc���j��*�
�Eӛ��6���*3O:�\�׺*�>򾂪&�(�p��sYg���罴�+�/kʖ�y|�k��2p�@�u �����/�P��Ҳ�t%r�0x�g����͹}9�xm�^<�Y�h��$
	z1S������o��4R�]�~�f�鬬΢�='W۴�M+����b���B��{�K�������Z	�v)<�ϫ�u�� ڻ��<��Q�PY�� �j�w=��ǚ��2��a!�;w��Yr0�N�yQ��hqc���Ve�ט��I�=�yXH3o�̋t��&4#Z]I�#R�~JI��6�ë�ar���=1��Ѷ���ȍ��1���0Q��wZ�^fS`9����(_ʟ�c�-o�(x���V��N��Rօ�7T��[��V�\�Ѩ�r�Ӥ5kd�o���F����J�Dirx��Zn-+"����	��7הO��й� A��-@�d��G����?����h�k^o�����?:>��q8
J��[�@G&G�H��?H�&���P���4Z���9z5TJ�2����CV��C� �~+g5��2w�ԄN��V��D�)��N���ӈ��gU�
�Q�0�Ϟ#���K���9Bv�z5W���8{"�'�t��� b�	�Utȧ�@+{�V������M�X���Zh�rvV�5ы2��nت4�̏�D�b��I�N�KŐ~6[�m��П�-�18tR�Z�Ao���
�N�*�P���'��MO�WB(hi�|�b$U�*��ĳ`M�Ւ�A-��J��Pdxr*����^C�ͦ�[b�ŌL6n��
�ͦ�I�:�î�����E��6Z�)���s�V7\Q�9 �#-�K�Wlf��n�|�	S�)��Y�������<¹�,}L���O��ȳ�~�h9{�8�6�B�ƌ����%E�k��w��y��f��O�#���C�7Ս�����ƺ�mmW���С�M�����{��+m�*k�G6�O��	���7RN���W���rAdVR��e�\�M~��$b�L�s| RKa�u����Z�ΕG yV�HL����{�t`�o�\�0#���?XP�=Pk���Ʋc�(6��w���2�ʪ�+v�X�m��X��2o�K�~�K5Q��,�S�Nj܂��pv�Q��9}�˔�Fcs������֎ei�pr=��GФ"�K��9�˧� ���B����X�=^Eґ�g	��Dk�`��{���5��~"�(V[��@#ݪ��*��(,��C��
+t���6}i��T�i����ԅ��Qw=�c^%ꨔ?��3Oe�}�ADˋ{+�:�J�򂒺��[ �z�H����P���w�k�!���Rò+�h��h��i�˰s�	߿��Wliƌ��g%z���o��|"�/��^�_g����e�~7�3tz+��6�OK�x��~�5Syҡr/��G(���
��4 �b?	�'Ue��1�_&x�	;�kԊ������Y�?J�>q���j�c�ۚ�K�����m��J��Ѹ���A	�û_������1m�|��2w��G/���g"�Myq�]/��b{t�ro�J�r@iB\NՑHyʥ��-1�.�YU�'�޲�E�������1�����a3��	�!�W�?����
���Xl���rg]g��[���w�'�)�J:&���uj�`W�3{08�ԭc����]R?}������%�r'[;v�7_��I`z���w]�P��D�,�r)�(F����Nx���}���]��.c�g�s�R�9s*��x�`�P1��@uV!_��rG����I�]o��t{u��-�]�e��7���D�{m͇?q��G<�����8RR�{ẉnb��1fև5��� "�k���em��DA�g�L�F��W괪/<ja��3r��m�G��Cv���03�L�MEV��D�T�o1è��ff�xf�E�XQ�s�XT�?xmZ��}�cw��'��3�4ڌ]oԚ>��_�ߺ��^�Q�eZEy�@9:Q����^�]t�V`.*�>׸{��`�6���7��2�YW�y��l���=w�^������v���#�[��.cLW\T\[|�8Q,).���$&A��C��
%�?)������
����@�Ex9����Z1�\*SJ��@����sc*=���8��F�wK�D�R �-��^g��,����bl��J4F�Lnr�mƑ�F��h)�T�)6Y���jQ�-&�d����DΈ݁>���t3&�B<娒S��C�+b"�E��YdKHN�y�iz��}N#/4:�)"��͌�G
].G�i�N��5roeMň��L��K�gU0'���]T����װ��o�Og�.�q�%Mc���n����:�J�^����6E��h<e��z�hq8Z���j&�&����Hc(�TZ�T�b4;�]��wll�����}��[
�C-�Q�=�O�}���"`;'��%�;'���e��`?��`?�1��
�Z�42�R��e�A���Yo0���v�6�A:%���O��d���G�=�c�n�ͼrR�T�ãP@vTj�L3�Z2��:����������@�K���d�u�F;[��e�n����u8��;k��-��z��BoRHzuA]W��kh��$��!�":L�P��]��y$�pHj[*��X�`��3'�.!	�0�x��w4���-G*3ý���o�������N�j)�q��`�B�Qv���8���MUpQ�y����흣�߶&�J��	���5�[�Z�u۳��u��Ag1�R�^�g疽ZF���G�f6�B�V��V���GSy��D���?��c-�|k	0�,���s��*�L�G9WV��e9C��W���N�R)�S�j黴*p�c��[q��� �-e�Ԕ���y�y��f���i��~~N1zd��sM���O����+�S�$����R*J{B�*NĤI$ĺ�C~������N��f��Z� -�������Q��<Dn����?����':v1`Z�ւh�� vcH�?�\����ҟ�@����@������l�G�g|�b�r��˃_P_�<�M�kV�aOi��vܜ�Rw[�x}`�ax����<�:C��p�ѕ��L�,�0\�d�l��[﷝����p�ׁG
�������=�M���K����9����zP����u��Oy_�A�O��ȇ
�E�e��T��z�@���j�m5��k;��M���m��\���xgh�����O554=���&˦)�lnh������ /�̴���������C�h��hW�7�] ���i�e�������q{��:��Tǃov2����Ώ|�k�k� �n��ֽ��t������N��ݿٲ��ؖn�Ԗ�{�=�K�z>��`ϛ�L�-����P��z��7�w������o`l�Рa��!���>���m�ۖ�-7��}x��v0;>�S��k#w��=��+W�-]�{p��v�z��/�޿G�Ǽg��M�s+����޳�Q�_�����r�0�/�.<�ߖ���K���/���
\{��W�?h>��<x���W�r��k�y���`G�7��y�P]�9�z$aK8~#r|�"�M>:���1̃����ӷM�o|t���tx��'b�طW�L����7���}�'�`9q6��ī��6��8����~��ȳ g0�x��G~|�� �u䭤(�0�pw�����!����0|%}~n�ܳs���m�kE �][y�u�p	�.�O��8��w1���#8�����%xl�w�\���5�{������p��Ϭ�/cxu6`6`6`6`6`6`6`���l�_��k�b��,J2,.���8����O���S|Z�WGB������y�2j^�&��S���|ZAq�������l}�[�i>��*e���T.੥�B~�8-���i��Y��4C�l7�ie�����yu$��v���˨V�C|ZN�-�|ZA����i%=�����lo�i5e����F&�7�i-U
uD��$g�Y>M�L҄�$M�L��:��$-�+'|&i�g�&|&i�g�&|&i�g��hm�f>M��OG��:��j��v*J��$��R��JCY���,�BIRq�W�� G�B�$5�R8��Ԟ��0��P����� 5vBo�c��S5=/B�sx��&1&�O@�Eh+��eq��hMi6�������Y����A���u�Bn
J��9�/��g�G1���3���Q[ ?WPisa%���O)�G���!L���h��%sP+���A�.�NN�;Q�.��ڊ�Gp�5c".��'�c$��py
�4
���с���(�Lz05QLI4KG��@�!�'���xYG�G�k꡾!� �4�C
��t�ļ@�F�s���5�i"c�1E!�i���r�R����s��)�o��E�Dx��Z��^���"�����(3�O�g��2%3xT�g
s*�q�BlC�-�=��i��������8ǲ�����B���J`ގ�9��)B\��#T���n�4�po3��Ė9�J��-h_��dD?�Kk���,k���Yj��|���{ODB�Y)�� �YA��yB�I����a�2�e����W-k���k���MЋ<��5=��cMD��� g�k��$�׳��Hs���P?�u����Unx��g<�0`�ʱ�U��9j kEc�@����cޢ�3k����\-��Mb-B�Y�� �Nx,�J��a[��H_��h
��,��pAh����A<�"�4�L:+m���B��FV^�y����Z��g1_� �D�|����Q��B��8�C��j���D�kJ&�4T_�' Q!�y���O2nuv��/�������xJ���bئ���=jC"K9ԯX����Np�Ky�o$�s||NcɅV�����j�Z�t QBh!��W&�3�0��q�G����^p�V��?	U$=����0�cQ޷�~P����Q���dr�͛ULa�������O�0���R���d�8����j?���W����xF��GRB��$����}Z�;+x��y��l@��ωN�8�>��>8WV�����I�2;��Q$�ݗ�p�V^<�!ɍd-'�7!�&Z��";�˽Ӝ䣏0� �I^΂����;d��w1����\�_�����r(�iG|��>��j��k�1��13�g�)��<��-��V�y�vE��yw��p��Q�����ޭz�wx��u�DW�-�����&�VS����<���_1�oSy�`=�q��j.+�|_BdX�K<��$��A�땺t�\͏����H�R�s�X�|���(D�9|wI8�� �?ј9�LC�P^�H_����e�'��y�^o��1B�2��gB�Xϧ�l�¾��j��{����D�Y�SXK�wbEk�|�R�� Շ���!���(.�2��(\��^(텒2�1�_/Òڃ�� Ի�8��(|��>���)�Qn��}��}�^<F�6�k�⾷C�0|���P�(��(=�� o�"�C|L$��r.K�J����f�!7
��W���!���ߏ�;�x��vc��Q�=��0Ρ�+�{���1����~�Nh����}<����n�
��o GU7�� �&ǿ��Q�pu�;�e/�ts����v�rTI�`jWz!��dy7�?	.�y����|=W�����`���9"��ۅe��V��t�u��>\�S<�Ր~��{A;�;�0!�!���"h5w	!�ׯ�%��/��ݘ'�����l�8]}3�=J&R��4דH�&��t4�qݱ7��J���H*����}���x2��휍�w-�F���bb.����J�.&Q�\��kS57��Nq��x(:�[Sqnp.�B�욊��X~?�$�%:���1��$`P.��K�"Bw!��ps�p$ɥ�"���]�p4��"�\*�"3�p8�b��GR�dt���G��h,��	Ƣ��(#��$�C'OA/��7�����hz�K͍�c.��q��I@
��#3�2$�d�����H0=����d���a�P��K�����,�Q���X::]��f"I����q)n6� i l��X,��Ms���l0��q.�x�A�1c%&���$���\�����ǓY��f��E.4"%x#�Ł�� В��G#�nn=NBI*zTO'��yDR�̐��򄦂I@,��F&�b�dV�Z��[�>4�!4����O'���L0yсE���I��,*%��x4��υʃ�
�"7�L$�S��l���6��|3BK4�M/�&&��٩���8��
5cs�`j"�C��`����X]�q�s��EnT(��#F�@��H5��fA��@g�Q��*��#əh:ݍ/b�uV��$�Bb�P��vЃ�\(]��q�V�6�  ���hh*�4��@�s�'�)��
byա�KaK�t�J'�!��� X��Z1ʣ0
�r%Id9��B<��Wr/HX���Pb.=^ Ad�:S���J��_�%Ց@��N����4�O�]��DYB�gu57L��x�SB(�u!�-DGg#�hЗHN֢\-�<���
/Vl�����z����0��"b�thB�[��c��^�&+W8J�f	'���D�(6p&\�M$��!C����W Qh�%����S��Qzv�T ���T""� ;�O�?�ƀ3���rc��~�c�ސ�a�z�Ϣ�<u���a/\�EAO�ب�$�T06"Da5���	�����RS�`���9d�)T�k	PX��"�E'f�ģ^Ub�0$1�������%hDf0��2�A8>�2	���1(8����8���H^��'��d�3��fL4����B�`<��r�y�&����n�<��H����=y���"����!*"9(I�(@E%����qPTtQ0�9bZ� �����eM`�`XEE�n�0��>����<�{�U0v���_��ު�i1E���<5 ��y�
|���]��B?ߑ�.�.B#� H�
�==|��P���'p���M��3Z8����T�:���5 @��/�����t�<Og� Ow�����'X"4�+�.�h��5�j�������N�^���M�n��>T�nШ����?��9���_�����
�w�f}<}���*�ޮ>����@��u$$��^^������t��}�F�{�{
=|�\\!��z����*�@9{9zz�
]��]�|����w��t\���=}}(g_�@H��`������BG� j@��}�yj8�_�8��U�
5��/f�P� ׎���:zA[��ʕ�U�?��X�������c�������G����x�����?�ڛD��#��������c��	��=& ۔�k�a�ZX:���+~#C��o=������`���5�n}�>ݑ�U_M��_�w뫫S���~�NT}f�߭����{�zC�A�g��5��	��3���Ў�
]GX8|0;,�l2L�LpV���X���.p�����XR�n!u�)��^��f�Q�BcQo�,�L4�B��\�2P�D1(%��h:��#��m�0t�B�D0�H�B7�t�E�TO�C���8"rpu��"���܂hćM��M4����T���/Y��:Xk�n�"`=���X �K`mV�vV`�=�zk0�N �`Mօ@���u'�k�^֛��X��5�~$��|���k_` �����c�u
�&�<`�~��ĔX�ko`�VG`�ֱ�:X��5X7�^`=��{X�+`��ԑ
�F݁���:�?��k�J�u���]4%5���e`�GO���s�`�31
�I��܅��Dn�C��XÁu
�&k:�f�f`-�c�
Z�/}�ʾ���X����b7`�H`��`]����X�@�=`m�V�#U���| V7`��	�� �b`��-�Z �ǁ��� �����-�����j�V�� �������u<�& �B`]��u/�����>֗���KV�E%��j���u8�F�,`M���Z����X�a���%�nX
�"����XÀ5X��`]����������X[P&.@Yxw����H�;�/�F�L`��K�u%��֭��XO�`��u���h$�DуxG�̈́�p?��%����.���p`����X��^`=%��`D`!HXE������5X7k!���*`��o�L��f�h.n�2���:XGk���4`]���X/�m`} ���X?��DaD�"��p"^�	�3�u%�n���z�Z�8l�RW76v�#�p��î��j�J�MT�/C��s�h��K��a!'--���8qbE��!�݀4+O���%�p�WZ�5tee[�fggf҉�4:$��З�Z��C'��R㰚msX�H�� I�4�D*��JXL�b7q��R�-6tWJ��b 3��c<�ϡ�@%�~��Y,N�0��C�'VP�䌘�Q��A,�������B�.�b˻ �	�b��O�����2R������eI�L�v�dc1�X,.��J�Rq8�^����	C������S^W� P�8������*�2�Z�2 E:IP�����ˣ�F�! �G}����Q:�'�9E5����jVWg��980(M�
j� �?�h�m�B�����9v�済�/��7C̆H��c#��E��.����{��1 �H�L{\&����c��Gp��G�e5Q��Sȯ��o菋���
���B�W����m��D�ʽ�k	r�vH������6�Eȕ�&�C���!]�&ByB!BH����c<Z�L�1dB���"��q�L"��ͧ���B\5b� �f.RvNtO���yi�EI�q)�|�>��j>��PK��&�4��C\�B�C��J:fB�r�W���"#c��t��)�
pa��C�]�SRiZ��qٟۮD\N�������S*]&qq16���LĦF*	f��B<�u��);J�ݽ4�.b0��P���f!6�[��9<�c����F�'�(�*�!��1��؂b��6Cy�[V��vj����d �B��1eKaԨRc���n�>�L�R���y������OL�N����c��W�
gP�c#ĆS���� (��h#�V�@<�PI�B:�:�(b0�����B�R�P(Yج()SZnO�b�晭el��!m�p@�|�\��Ϭ��M��0�Z���w�y>(��6�qi���J[xH�;ʻ�hO�`�f*M��(ɵ���j
��WoW5}nZ��M��OE&��[!\!\1"�(%l��y\���+z�1{�n��\�����Ixl��i��:�IZ����v��+�Ęb������
��e�ok�O�-h�M�_��������ܩ�&Q�N��X�|�����7��o�;_I��+��9��!x������T��(B&���5�(��skqK{2	&�G�]�l0��^I rW��5�S�����<lЩ��A<_}u;�و�P�>�=�� �=�Y�@a|.��;��UiJ��bZ ��@_J���%|�W�iɴ��<�<(�_�Yȑp���y� J�i%S�t��8b�3�`�����"�1������K�L�M�7�W:�T�*�F^U��=	�H��+�Z�ʎ~�1�Kq�ܨR�A���.��@)�Ŷ�j�jL"�;�v8B�Qs��������m�ު���ž��QB��oT��X�7���)�	����Y�/[�y�� �:�x��p�G@]u��0�6+ \�j爐q�a���%;�ّ�͎��Z5	(;j3$8�y�Q�!і$`S�Dϱ����%��S��N'��t0(c�H�5�xZ�w�����KZ+���J�9!V�9ɏ)s�1_S��{*��"q�l>�vʻ8H�k)///k)/---op!C��a2�9z=����N�!�,�!����V�r�0�_d��XZ�!7��ziyeeuSuueyy�@	�kuju��L��UO��,�<�Y*(���5ɪd�+!�C<#+���|$P�æ+��b�l��-���=�([�r����u,O��L�m�觖���QQvZZvQQ��^��.[bT�	Q���rk^y��Y*�£.y�q)ߖoB��~D��������I���"�.��z��
f�.,,�9L�n��TG*���GZ����U�]��,�"�������(�8�N�T��6�����mk�ڷ&��j�t�I|&,����R4L�{���8 �D�*|QS�5)72תЮI+L+L�U��XL�LhV&_�eR��K9.&]����ˏ芈���&u�H*C���3�#E�ʙ0МJ*�ӭ����l�����Jg�)�Yc�ZdXGˎ��sh���.�j,
sy��Ya�Se�җKUe�R}�5�C�j�~�N=�#��NR�ϐ����'�
bbM���	�L���ҟ	�0���v5z�'����t�����jʻ��CJtdq��{��SAl<O��Y���I.�i�J��L�g�LX01����R���b̎���s�8�7%����T$��chn!��xp�G�ӫ�1�pn�D+��0JI	�'�Qq\��X�$�fjG'�.'U�{�#g��$�,<(@�Av�^p���ѱ��bE�*���`�O������$u��F�o�b"�'��rBC��<0:f�Y@bxL���ّ��ME4�Hڈl�m�-C i��$S������|�����������ɞ����ԯ���
]|�Y[ؚY��ؘ�:��&�D:�$
��?)A��G11B��0�����}|�;/H�5<(�<��f<�qQ��wY�a����T�n������`����Z�Z皭z��@�vD�u�#?y_�l�ӣ���4�n.�]���x˱���d�"�۞��i�4��L���Zo[sB�L|yXX���J�dr���ߓ 3��Y����Vқ{gg=��6��n�K�_=7�|��B?�M!�!��\��}�O��=�3[�\�x�R�L�SQ��1�k�ݺ��1e�o]�d�__�!��_�֩2�Nu��9W��V�O�n������`G[$�#�$uaHuU]��N��(���w�~iZ�!W���5`h�]ŚVͿ����>��XlRXj]�FR���p�3�=�5�Y�;�	ӾzQ$~j4��_��Ō���H�"=��Js�B�bq�0�L��`x��H��4���).0{��o]`b�_��HjP������&	�WIP*��n7n�X��o�lCY��S5��zg��mo��R�2�#����*ؼ�n�3�A�w>Q��X�>�C�]��μ���5�������z�i�o��ɪ�����cVx���~.2	Z��L��4b���e�\\�n��Jw�-����j�Zjĵr����Cg�������i3MscEҴ#�w/J�by
����0|'��lf������;o��,�of��r��5Ɍ[5k,�<p��?aj19�b��S�"G��yS!^��ݘ���R�yG��W�_������gJn��YFsJ�߳Vڍ�)��ؼ�Y�}�F��\9Q=�~�&�z�ND{3�V$� !ZɽYG�L�W��('���?z#�⣆���k��]Z���$HM?�ْ#]�vd����Y��\��a�.=	:�rQ�q����w���Z{�濚4䬑�#c��َ��u�l�Xk}�6>0np�>W.�Yrj9�Fpq��w3Vu��˒���8�=wZ��~�6����u7�>/��/L:��Oz�'�>�V���F������7���q����S/���J�U�q�%V�ᵅm�h�ʧ9�+�<X����jz˶?L�Vr��&]t�����9��g7cN\X�74��6V��x�����aD���Mo�ݴ��^�n�����xcB�封�['�s����#���?U܉�h�;���JcEZPI����%I�,L"lI�	��ͬN�2����5��`aik-�
��������z�F>�c^���fc��P��3�U�����g�^�:��)���>�H3Җv��J.0��݊�t��h�q�DR@u\�VNb_�3!���w+��_����I�64���u���=F6TD�3��]��߲&t��N��2��F��d鉨=����AG�$9��o~��d�Y�S�]U�Vǅܵ��c�X-ٴ|�M��NA��?WK�wY7��U��p{�#��Q�����wI�<������F�euɬЍ82C��FJ�~�]wX,�_m�9� �s���ŏ8]F�5	���z�V����q/��??�ڭr�O�@m�e��bd�F��Fz�]�����k��O�� ��1��������<D�$Ws�,��QR�'��Y��¤���W6���fƓ��&J'�uN���	G�+����x[��밟l����)��y����Eǧ._0mQ����>n��}c`K��{Σ9����r�˫GnMu����+��-ve"������l����q����/95o��s���ژ[V�y1����<���m!S?�s�ճ*Nr�>�}�ց���_;�{��E:��S����3����:h�V��Ť2��o�^2d\U���
�+�$��e�f�|����;�eb3,lX� /��d+���|��O�Swe��_�F��]	P��;��Ln�XA�&r�i��7����y�t���#�'
g&N�K�NL��;iCZ��"kKr 8w��$��o������iE5�<V��3ռ�����]3��oߥ;Z>�j/~��׾DRة�}=pU��N+��!��Ħ>��d}[�*#�)�R���L�1m��T���-�%�~p�̭WPU����~��'�j|�-�0�ꑱ����t� �C��㔬,2v�����n�?�ϙ�|E�5�H@��A׬M�0��NF}�v�<��J��}ڎN�\ɦ�����h��g!�N�5�k�v��,pSA�$G���u5�����U)jy�� ��kx`�{f�!�Ϳ��A��{&I�?J����K�}�1��tR��U�	]�����rߜ�E�.k�9�4�y�[���=^�����Gl���)QO��5X޶}^3F�ak�O$�䋂'	�P�s�c�п�/n/�޼�\9� *-�颴 ���=1��,o�o�a��s��!\�yvp��[��Gx�"���1�=�N������Λ3c&�/�5���Iq�|�`�Z�{�(}��WK����O-�1+�z�o
�r�w�ʇO�N�..y����!�lE?�^�߶<LZc��}?���φeSy	���\?������횻D8�>[��}�h�,��~���!�y5gx�˚~=ڭ�g����&㶜�;1���õ����IǄ�n<M�+75s��)jT�Y�'��W��tC|������M>�[+eB�����Z�fkO8?�g�������e��G���z�ug��Q���:��ŷ�Ϝ��y����{R�&�Vq��xc2�S�q�{�W9?3yv��G��j�W�~��C��l�~w͆��N�%�:���z���(�pє!�����kl?�۽�sܧ��|�Q�ip>���E�#�!f��}���Pᅈ�I��k��~{��%�)�[=S����4f��o������t^c��u=}ϯ}�Y�M���ϭ��x�|G�%Q�Vճ�c��{�W�q�yPש�5�|"%�Rж�f]����ۀT��-HRn�}��Av��`ٰ� ���tRDR������ځSkk�ܞ�	�:���cwKԽ���:<J�S�~S����>ʲ�fx�_*�y�fjy�j~��5��ב���j�Jr�y�a��
6z�6yܕ�ux����2ٟ�-�u��a��gQ��Z���������b�#c��̉�{&���zИ��o܎��F�Nڞ�fv����w�*��$o���D�T���S�C?>0	Q��i�9%���#���W,��?���;(s���4�W��G?�l��r��#��-�C����we���w��+��{����pl�ھ�i�#җ��T�:3{�	�~b��ZƇ+��m{�6�򜢕�uv슪כr��s�x���c����/;<Ԑh�%%��u��c�F��.n��؋K�ߒu)>��Z��'�՞x��:�2��aIiBJm�Ú�nk�6��	��`i��'�cϲ���M-w
�����p�a�Ͼ;4���;I�x������~�����/bJ���.w��-���%���u��6������6'	G�j�[����2�f���ݍ>oV�p˛�{���4�}�l����7������%��O����<,�~��s�r]�â�|Ǔ`6e9������|�9�/Vd�|q�~���7<����������d<i9�^��)-s��飴�9��e�/�O$S7Q�2Rs��l2uE� �d�rh��p���?�fQȢc��#�g�ON�!��I��B]��� 3�n�x����`ɐ��xKmb��z�B�o݈Mz��-�60Y��ju�^���;݋X��i��+ɂ�����M�K~�Y���Ч��O����:�V��^��r�NL˚���/�Z�r���:�휖�W~����m�w��!=�];�;;{��g��]�$��֘�=+q��7��n��,V?�uS��a������7u�g�7:6$w��od�_���m\uҺ1���GFUw^��1���V��ɸ�Wj�u��٥Ѝ=��yg���t�[]�#\G�ZL7Ҟ_�ƨ��� at���c�vI,u`���~�����Q|Y������׉�2�uǬG�&n)�?!�T7b@Nz���ͯ��5��󶜪c#���/�g�f��*���y*<�P����S5��T�_ܝؿ>�m����؍|���_�l��P_#֫���-Z�m�����W6oޔ����*�=�Ŀol>=����u3���۬I��z��`���Z����ϣ���e553c"V�e�H����^�I�,�SyEC?��:�$_�.x�HW���u�Byb����7�����r���J���"	���0�������׷��p$/��r>
s	�@����#���ʥ]H��"pm��]v,{��Fj皾'c���i�%#�N�F��y����������}Ćjف��H���̐ ,�}���7ƅ�n����?^<�=T�����{���6Vj6�W��X7�Wty���ktB�����}�{���>F/Z�>�|e��[g3j&7���{�¾K�����1N|:q䧊g��.�n>9�!r˕�禝����c]�rl�5��^5�/�T��<����z�|zN��|f��5�}����lgG��8��1Eǉǚ�Y�C{4���r��i�����AG��9���N�����1͇�d�ݼ��S팧ٹ?'���ә*Q��.��g�V��>���MC��Kpc؞v�K$��@V'Z���k7��~Ҧ�ɱ���$�O\���)R�p<@dm!�B���,m�F?�su}2��^�M�]w8��[&J+"��xF0�3zXNbo�����}ύ}}���s�d�3xj1�s�����K}zO鳥f�x��+�M���ۃ�y]c�;v�J�����w��j�����C6����<�]���x�g��%��$�ˉ��71Ԙ�u�@EԆk/��:�r?����G�$�E��|�����+�W��}��O�eɿ|���(����������N{�������:���L]_9��g[���R���-�\�Q�N��b���wpZ���l{ĽA����:�xj,8����m�Eo/u����b
endstream
endobj
68 0 obj
[ 0[ 507]  3[ 226]  18[ 533]  28[ 488]  44[ 623]  58[ 319]  69[ 646]  75[ 662]  87[ 517]  90[ 543]  100[ 487]  122[ 487]  258[ 479]  271[ 525 423]  282[ 525]  286[ 498]  296[ 305]  346[ 525]  349[ 230]  367[ 230]  373[ 799 525]  381[ 527]  393[ 525]  396[ 349]  400[ 391]  410[ 335]  437[ 525]  448[ 452 715]  560[ 579]  562[ 544 416 564 488 488]  568[ 623]  571[ 252]  574[ 520 573 855 646]  579[ 662 662 623 517 459 487 487]  588[ 759 519]  591[ 664]  626[ 567 567 531]  630[ 446 523 456 456 348 537 537 532]  639[ 274 274]  643[ 455 463 550 449 376]  649[ 527 527 553 509 532 411 387 542 542]  660[ 651]  662[ 426 708 696 696]  853[ 250]  855[ 268 252]  858[ 250 250]  882[ 306]  894[ 303 303]  1004[ 507 507 507 507 507] ] 
endobj
69 0 obj
[ 226 0 0 0 0 0 0 0 0 0 0 0 250 306 252 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 533 0 488 0 0 623 0 319 0 0 0 646 662 517 0 543 0 487 0 0 0 0 487 0 0 0 0 0 0 0 479 525 423 525 498 305 0 525 230 0 0 230 799 525 527 525 0 349 391 335 525 452 715] 
endobj
70 0 obj
<</Type/Metadata/Subtype/XML/Length 3063>>
stream
<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?><x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="3.1-701">
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:about=""  xmlns:pdf="http://ns.adobe.com/pdf/1.3/">
<pdf:Producer>Microsoft® Word 2016</pdf:Producer></rdf:Description>
<rdf:Description rdf:about=""  xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:creator><rdf:Seq><rdf:li>george siozos</rdf:li></rdf:Seq></dc:creator></rdf:Description>
<rdf:Description rdf:about=""  xmlns:xmp="http://ns.adobe.com/xap/1.0/">
<xmp:CreatorTool>Microsoft® Word 2016</xmp:CreatorTool><xmp:CreateDate>2019-11-29T20:34:12+02:00</xmp:CreateDate><xmp:ModifyDate>2019-11-29T20:34:12+02:00</xmp:ModifyDate></rdf:Description>
<rdf:Description rdf:about=""  xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/">
<xmpMM:DocumentID>uuid:25E5E231-893F-4BB1-96C4-618FE3F813FB</xmpMM:DocumentID><xmpMM:InstanceID>uuid:25E5E231-893F-4BB1-96C4-618FE3F813FB</xmpMM:InstanceID></rdf:Description>
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
</rdf:RDF></x:xmpmeta><?xpacket end="w"?>
endstream
endobj
71 0 obj
<</DisplayDocTitle true>>
endobj
72 0 obj
<</Type/XRef/Size 72/W[ 1 4 2] /Root 1 0 R/Info 21 0 R/ID[<31E2E5253F89B14B96C4618FE3F813FB><31E2E5253F89B14B96C4618FE3F813FB>] /Filter/FlateDecode/Length 212>>
stream
x�5йNq���.����!���p<
	@Og| �X�ۙX�ZP�@KhxL �M���+S�'��d&c���ֱ�3f�+l��~��)�X���E�KQ���J�oEg*zob�$^��ݮ�GT�%\�54��;�v��y_9�B�p 1�C���C8��	�!d!��(@JP�8�
T�u8�б�wt�G�q/�#��_cc� o+#�
endstream
endobj
xref
0 73
0000000022 65535 f
0000000017 00000 n
0000000166 00000 n
0000000236 00000 n
0000000520 00000 n
0000005712 00000 n
0000005842 00000 n
0000005870 00000 n
0000006027 00000 n
0000006100 00000 n
0000006339 00000 n
0000006393 00000 n
0000006447 00000 n
0000006617 00000 n
0000006857 00000 n
0000007143 00000 n
0000011633 00000 n
0000011976 00000 n
0000012464 00000 n
0000024465 00000 n
0000041811 00000 n
0000064441 00000 n
0000000023 65535 f
0000000024 65535 f
0000000025 65535 f
0000000026 65535 f
0000000027 65535 f
0000000028 65535 f
0000000029 65535 f
0000000030 65535 f
0000000031 65535 f
0000000032 65535 f
0000000033 65535 f
0000000034 65535 f
0000000035 65535 f
0000000036 65535 f
0000000037 65535 f
0000000038 65535 f
0000000039 65535 f
0000000040 65535 f
0000000041 65535 f
0000000042 65535 f
0000000043 65535 f
0000000044 65535 f
0000000045 65535 f
0000000046 65535 f
0000000047 65535 f
0000000048 65535 f
0000000049 65535 f
0000000050 65535 f
0000000051 65535 f
0000000052 65535 f
0000000053 65535 f
0000000054 65535 f
0000000055 65535 f
0000000056 65535 f
0000000057 65535 f
0000000058 65535 f
0000000059 65535 f
0000000060 65535 f
0000000061 65535 f
0000000062 65535 f
0000000063 65535 f
0000000064 65535 f
0000000065 65535 f
0000000000 65535 f
0000065570 00000 n
0000066189 00000 n
0000125055 00000 n
0000125802 00000 n
0000126067 00000 n
0000129213 00000 n
0000129258 00000 n
trailer
<</Size 73/Root 1 0 R/Info 21 0 R/ID[<31E2E5253F89B14B96C4618FE3F813FB><31E2E5253F89B14B96C4618FE3F813FB>] >>
startxref
129671
%%EOF
xref
0 0
trailer
<</Size 73/Root 1 0 R/Info 21 0 R/ID[<31E2E5253F89B14B96C4618FE3F813FB><31E2E5253F89B14B96C4618FE3F813FB>] /Prev 129671/XRefStm 129258>>
startxref
131289
%%EOF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 