from collections import defaultdict
from string import ascii_lowercase
import sys
from abc import ABC, abstractmethod

exit_conditions = [":q", "q", "exit", "quit"]

class Product(object):
    __product_name = None
    __product_price = 0
    __product_quantity = 0

    def __init__(self, product_name, product_price, product_quantity):
        self.__product_name = product_name
        self.__product_price = product_price
        self.__product_quantity = product_quantity

    def getProductName(self):
        return self.__product_name
    
    def getProductPrice(self):
        return self.__product_price
    
    def getProductQuantity(self):
        return self.__product_quantity
    
    def setProductName(self, product_name):
        self.__product_name = product_name
    
    def setProductPrice(self, product_price):
        self.__product_price = product_price
    
    def setProductQuantity(self, product_quantity):
        self.__product_quantity = product_quantity

    def print_item(self):
        print("Product Name: ", self.__product_name, " Product Price: ", self.__product_price, " Product Quantity: ", self.__product_quantity, end=" ")

    def __repr__(self):
        return self.__product_name

class ItemShowcase(ABC):
    @abstractmethod
    def items(self):
        pass

    @abstractmethod
    def addItem(self, product_name, product_price, product_quantity):
        pass

    @abstractmethod
    def removeItem(self, product_name):
        pass

    @abstractmethod
    def clearAll(self):
        pass

    # @abstractmethod
    # def display_items(self):
    #     pass

class Electronics(ItemShowcase):
    items = ['washing machine', 'Refrigerator', 'Mobile', 'Laptop', 'Mixer', 'Oven']
    price = [20000, 10000, 23000, 100000, 2500, 3000]
    quantity = [3, 2, 10, 4, 3, 1]
    electronics = [Product(name, pprice, pqty) for name, pprice, pqty in zip(items, price, quantity)]

    def addItem(self, product_name, product_price, product_quantity):
        product = Product(product_name, product_price, product_quantity)
        self.electronics.append(product)
        return product

    def removeItem(self, product_name):
        for product in self.electronics:
            if product.getProductName() == product_name:
                product.print_item()
                print("is removed")
                self.electronics.remove(product)
                break

    def clearAll(self):
        self.electronics = []

    def get_items(self):
        return askItem(self.electronics+['Back'])
            
class Groceries(ItemShowcase):
    items = ['Rice', 'Dal', 'Sugar', 'Tea Leaf', 'Wheat', 'Corn']
    price = [45, 150, 50, 200, 40, 40]
    quantity = [50, 20, 30, 3, 50, 30]
    groceries = [Product(name, pprice, pqty) for name, pprice, pqty in zip(items, price, quantity)]

    def addItem(self, product_name, product_price, product_quantity):
        product = Product(product_name, product_price, product_quantity)
        self.groceries.append(product)
        return product

    def removeItem(self, product_name):
        for product in self.groceries:
            if product.getProductName() == product_name:
                self.groceries.remove(product)
                product.print_item()
                print("is removed")
                break

    def clearAll(self):
        self.groceries = []

    def get_items(self):
        return askItem(self.groceries+['Back'])

class Cosmetics(ItemShowcase):
    items = ['Shampoo', 'Cream', 'Soap', 'Powder', 'Nail Polish']
    price = [120, 250, 40, 170, 50]
    quantity = [10, 15, 40, 30, 17]
    cosmetics = [Product(name, pprice, pqty) for name, pprice, pqty in zip(items, price, quantity)]

    def addItem(self, product_name, product_price, product_quantity):
        product = Product(product_name, product_price, product_quantity)
        self.cosmetics.append(product)
        return product

    def removeItem(self, product_name):
        for product in self.cosmetics:
            if product.getProductName() == product_name:
                self.cosmetics.remove(product)
                product.print_item()
                print("is removed")
                break

    def clearAll(self):
        self.cosmetics = []

    def get_items(self):
        return askItem(self.cosmetics+['Back'])
        
class User(object):
    item_bought = []
    add_to_cart_list = []
    def buy(self, model, product):
        if product.getProductQuantity()>0:
            exit = False
            while(not exit):
                quantity = int(input('Please enter your quantity: '))
                if int(product.getProductQuantity())-quantity>=0:
                    self.item_bought.append(product)
                    print(product.getProductName(), int(product.getProductPrice())*quantity, quantity)
                    print('Thanks for shopping')
                    break
                else:
                    print('Quantity not available')
                    answer = input("Want to continue[y/n]? ")
                    if answer.lower()=='no' or answer.lower()=='n':
                        exit = True
            answer = input('Want to shop more[y/n]? ')
            if answer.lower()=='yes' or answer.lower()=='y':
                self.choose_items(model)
            else:
                self.display_category()

    def add_to_cart(self, model, product):
        self.add_to_cart_list.append(product)
        print('Items available in your Cart')
        for item in self.add_to_cart_list:
            print(item.getProductName(), item.getProductPrice(), item.getProductQuantity())
        self.choose_items(model)


    def ask_category(self):
        category = ['Electronics', 'Groceries', 'Cosmetics']
        return ask(category)[0]
    
    def choose_items(self, model):
        answer = model.get_items()[0]
        
        if answer == 'Back':
            self.display_category()
        else:
            self.operation(model, answer)

    def operation(self, model, product):
        options = ['Buy', 'Add to Cart']
        answer = ask(options+['Back'])[0]

        if answer == 'Back':
            self.choose_items(model)
        elif answer == 'Add to Cart':
            self.add_to_cart(model, product)
        else:
            self.buy(model, product)
    
    def display_category(self):
        answer = self.ask_category()

        model = None
        match(answer):
            case 'Electronics': model = objects.electronics
            case 'Groceries': model = objects.groceries
            case 'Cosmetics': model = objects.cosmetics

        self.choose_items(model)

class Admin(User):
    item_list = []

    def add_item(self):

        category = ['Electronics', 'Groceries', 'Cosmetics']
        answers = ask(category)

        for answer in answers:
            print(f"Category {answer}")

            model = None

            match(answer):
                case 'Electronics': model = objects.electronics
                case 'Cosmetics': model = objects.cosmetics
                case 'Groceries': model = objects.groceries

            print("ENTER QUIT TO EXIT AND NEXT FOR NEXT CATEGORY")

            while True:
                product_name = input("Enter the product name: ").strip()
                if(product_name.lower()=='quit'):
                    sys.exit(0)
                elif(product_name.lower()=='next'):
                    break

                product_price = input("Enter the product price: ").strip()
                if(product_price.lower()=='quit'):
                    sys.exit(0)
                elif product_price.lower()=='next':
                    break

                product_quantity = input("Enter the product quantity: ").strip()
                if(product_quantity.lower()=='quit'):
                    sys.exit(0)
                elif product_quantity.lower()=='next':
                    break

                for product in self.item_list:
                    if product.getProductName()==product_name and product.getProductPrice()==product_price:
                        quantity = int(product_quantity) + int(product.getProductQuantity())
                        product.setProductQuantity(quantity)
                        break
                else:
                    product = model.addItem(product_name, product_price, product_quantity)
                    self.item_list.append(product)

    def items_added(self):
        for product in self.item_list:
            print(product.getProductName(), product.getProductPrice(), product.getProductQuantity())

    def remove_item(self, item_name):
        for product in self.item_list:
            if product.getProductName()==item_name:
                self.item_list.remove(product)
                print("Item removed")
                break
        else:
            print("Item not present")

    def update_item(self, item_name):
        try:
            item = [product for product in self.item_list if product.getProductName()==item_name][0]
            operation = ['name', 'price', 'quantity']
            answer = ask(operation)[0]

            match(answer):
                case 'name': name = input("Enter Product name: "); item.setProductName(name)
                case 'price': price = int(input("Enter Product price: ")); item.setProductPrice(price)
                case 'quantity': quantity = int(input('Enter Product quantity: ')); item.setProductQuantity(quantity)

            print("Updated")
            print(item.getProductName(), item.getProductPrice(), item.getProductQuantity())
        except:
            print("Item not present.")
        

def ask(model):
    labeled_model = dict(zip(ascii_lowercase, model))

    for label, model in labeled_model.items():
        print(f"  {label}) {model}")

    while True:
        answers = input(f"Your Choice? ")
        if answers in exit_conditions:
            sys.exit(0)
        answers = set(answers.replace(',', ' ').split())

        if any(
            (invalid:=answer) not in labeled_model
            for answer in answers
        ):
            print(f"{invalid!r} is not a valid choice\n"
                  f"Please use {', '.join(labeled_model)}")
            continue

        return [labeled_model[answer] for answer in answers]
    
def askItem(model):
    labeled_model = dict(zip(ascii_lowercase, model))

    for label, model in labeled_model.items():
        if model!='Back':
            print(f"\t{label}) {model.getProductName()}\t{model.getProductPrice()}\t{model.getProductQuantity()}")
        else:
            print(f"\t{label}) {model}")

    while True:
        answers = input(f"Your Choice? ")
        if answers in exit_conditions:
            sys.exit(0)
            
        answers = set(answers.replace(',', ' ').split())

        if any(
            (invalid:=answer) not in labeled_model
            for answer in answers
        ):
            print(f"{invalid!r} is not a valid choice\n"
                  f"Please use {', '.join(labeled_model)}")
            continue

        return [labeled_model[answer] for answer in answers]
    
class objects:
    electronics = Electronics()
    cosmetics = Cosmetics()
    groceries = Groceries()
    
def main():
    login = ['User', 'Admin']
    answer = ask(login)[0]

    match(answer):
        case 'User': userOperation()
        case 'Admin': adminOperation()

def adminOperation():
    admin = Admin()
    operation = ['Add', 'Remove', 'Update']
    while(True):
        answer = ask(operation)[0]

        match(answer):
            case 'Add': admin.add_item();admin.items_added()
            case 'Remove': item = input("Enter Product Name: ");admin.remove_item(item)
            case 'Update': item = input("Enter Product Name: ");admin.update_item(item)

def userOperation():
    user = User()
    user.display_category()


if __name__ == '__main__':
    main()