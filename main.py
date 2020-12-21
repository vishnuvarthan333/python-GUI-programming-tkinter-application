from tkinter import *                    # https://www.geeksforgeeks.org/python-gui-tkinter/
from tkinter import messagebox, Menu
import requests                          # https://www.w3schools.com/python/module_requests.asp
import json                              # https://www.w3schools.com/python/python_json.asp
import sqlite3


Pycripto = Tk()
Pycripto.title("My Cripto Portfolio")
Pycripto.iconbitmap("C:\\Users\\Vishnu\\Desktop\\project1\\Bitcoin.ico")

con = sqlite3.connect("coin.db")
curobj = con.cursor()
curobj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER, symbol TEXT, amount INTEGER, price REAL)")
con.commit()

def reset():
    for cell in Pycripto.winfo_children():
        cell.destroy()
    
    app_header()
    myPorfolio()

def app_nav():
    def clear_all():
        MsgBox = messagebox.askquestion ('Portfolio Notification','IF you enter Yes, Your All data Cleared from Portfolio app and also database \n Do you wish to procced?' ,icon="warning")
        if MsgBox == 'yes':
            curobj.execute("DELETE FROM coin")
            con.commit()
            messagebox.showinfo("All Data is Cleared from Portfolio -- Add a new Data")
        else:
            messagebox.showinfo('Return','You will now return to the application screen')
           

    def close_app():
        MsgBox = messagebox.askquestion('Exit Application','Are you sure you want to exit the application',icon = 'warning')
        if MsgBox == "yes":
            Pycripto.destroy()
        else:
            messagebox.showinfo('Return','You will now return to the application screen')

    menu = Menu(Pycripto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio', command=clear_all)
    file_item.add_command(label='Close App', command=close_app)
    menu.add_cascade(label="File", menu=file_item)
    Pycripto.config(menu=menu)

def myPorfolio():
    api_requests = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=100&convert=USD&CMC_PRO_API_KEY=6a478abc-aeb5-46aa-a56e-cd3a7a06cd2c")

    api = json.loads(api_requests.content)

    curobj.execute("SELECT * from coin")
    coins = curobj.fetchall()

    
    def colour(amount):
        if amount >= 0:
            return "green"
        else:
            return "red"

    def addcoin():
        curobj.execute("INSERT INTO coin(symbol,price,amount)VALUES(?,?,?)",(symbol_txt.get(),price_txt.get(),amount_txt.get()))
        con.commit()
        messagebox.askyesno("Porfolio Notification","Do you wish to proceed")
        messagebox.showinfo("Porfolio Notification","Coin Added to Portfolio is successfully!")
        reset() 

    def update_coin():
        curobj.execute("UPDATE coin SET symbol=?, price=?, amount=? WHERE id=?",(symbol_update.get(),price_update.get(),amount_update.get(),portfilio_id_update.get()))
        con.commit()
        messagebox.askyesno("Porfolio Notification","Do you wish to proceed")
        messagebox.showinfo("Porfolio Notification","Coin Update Successfullyy!")
        reset()

    def delete_coin():
        curobj.execute("DELETE FROM coin WHERE id=?",(portfilio_id_delete.get(),)) 
        con.commit()   
        messagebox.askyesno("Porfolio Notification","Do you wish to proceed")
        messagebox.showinfo("Porfolio Notification","Coin Deleted from Portfolio!")
        reset()
    
    total_PL =0
    coin_row = 1
    total_current_price = 0
    # total_price = 0 
    total_amount_paid =0 
    
    for i in range(0,100):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_price = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                PL_per_coin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_PL_coin = PL_per_coin * coin[2]

                total_PL += total_PL_coin
                total_current_price += current_price
                # total_price += coin[3]
                total_amount_paid += total_paid

                # print(api["data"][i]["name"] +" - "+ api["data"][i]["symbol"])                #fetching data from api-content
                # print("price - ${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
                # print("Total paid - ${0:.2f}".format(total_paid))
                # print("Current price - ${0:.2f}".format(current_price))
                # print("P/L per coin  - ${0:.2f}".format(PL_per_coin))
                # print("Total P/L with coin - ${0:.2f}".format(total_PL_coin))
                # print("--------------------------------")

                portfolio_id = Label(Pycripto,text=coin[0],bg="White",fg="black",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                portfolio_id.grid(row = coin_row,column=1,sticky=N+E+W+S)

                name = Label(Pycripto,text=api["data"][i]["symbol"],bg="White",fg="black",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                name.grid(row = coin_row,column=2,sticky=N+E+W+S)

                price = Label(Pycripto,text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]),bg="White",fg="black",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                price.grid(row = coin_row,column=3,sticky=N+E+W+S)

                no_coins = Label(Pycripto,text=coin[2],bg="White",fg="black",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                no_coins.grid(row=coin_row,column=4,sticky=N+E+W+S)

                total_paid = Label(Pycripto,text="${0:.2f}".format(total_paid),bg="White",fg="black",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                total_paid.grid(row=coin_row,column=5,sticky=N+E+W+S)

                current_price = Label(Pycripto,text="${0:.2f}".format(current_price),bg="White",fg="black",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                current_price.grid(row=coin_row,column=6,sticky=N+E+W+S)

                PL_per_coin = Label(Pycripto,text="${0:.2f}".format(PL_per_coin),bg="White",fg=colour(float("{0:.2f}".format(PL_per_coin))),font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                PL_per_coin.grid(row=coin_row,column=7,sticky=N+E+W+S)

                total_pl_coin = Label(Pycripto,text="${0:.2f}".format(total_PL_coin),bg="White",fg=colour(float("{0:.2f}".format(total_PL_coin))),font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                total_pl_coin.grid(row=coin_row,column=8,sticky=N+E+W+S)

                coin_row += 1

    #inserting data
    symbol_txt = Entry(Pycripto,borderwidth=3,relief="groove")
    symbol_txt.grid(row=coin_row+1,column=2)

    price_txt = Entry(Pycripto,borderwidth=3,relief="groove")
    price_txt.grid(row=coin_row+1,column=3)

    amount_txt = Entry(Pycripto,borderwidth=3,relief="groove")
    amount_txt.grid(row=coin_row+1,column=4)

    add_coin = Button(Pycripto,text="ADD COIN",bg="#142E54",fg="white",command=addcoin,font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
    add_coin.grid(row=coin_row+1,column=5,sticky=N+E+W+S)

    #Update coin 

    portfilio_id_update = Entry(Pycripto,borderwidth=3,relief="groove")
    portfilio_id_update.grid(row=coin_row+2,column=1)

    symbol_update = Entry(Pycripto,borderwidth=3,relief="groove")
    symbol_update.grid(row=coin_row+2,column=2)

    price_update = Entry(Pycripto,borderwidth=3,relief="groove")
    price_update.grid(row=coin_row+2,column=3)

    amount_update = Entry(Pycripto,borderwidth=3,relief="groove")
    amount_update.grid(row=coin_row+2,column=4)

    update_coin_txt = Button(Pycripto,text="Update COIN",bg="#142E54",fg="white",command=update_coin,font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
    update_coin_txt.grid(row=coin_row+2,column=5,sticky=N+E+W+S)

    #Delete coin 

    portfilio_id_delete = Entry(Pycripto,borderwidth=3,relief="groove")
    portfilio_id_delete.grid(row=coin_row+3,column=1)

    delete_coin_txt = Button(Pycripto,text="Delete Coin",bg="#142E54",fg="white",command=delete_coin,font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
    delete_coin_txt.grid(row=coin_row+3,column=5,sticky=N+E+W+S)

    #---------------------------------------------------------------------#


    total_pl_coin = Label(Pycripto,text="${0:.2f}".format(total_PL),bg="White",fg=colour(float("{0:.2f}".format(total_PL))),font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
    total_pl_coin.grid(row=coin_row,column=8,sticky=N+E+W+S)  

    tl_current_price = Label(Pycripto,text="${0:.2f}".format(total_current_price),bg="White",fg="black",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
    tl_current_price.grid(row=coin_row,column=6,sticky=N+E+W+S)  

    # price = Label(Pycripto,text="${0:.2f}".format(total_price),bg="White",fg="black",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
    # price.grid(row = coin_row,column=2,sticky=N+E+W+S)

    total_amount_paid = Label(Pycripto,text="${0:.2f}".format(total_amount_paid),bg="White",fg="black",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
    total_amount_paid.grid(row=coin_row,column=5,sticky=N+E+W+S)   

    api =""     
    
    refresh = Button(Pycripto,text="Refresh",bg="#142E54",fg="white",command=reset,font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
    refresh.grid(row=coin_row+1,column=8,sticky=N+E+W+S)

def app_header():
    portfolio_id = Label(Pycripto,text="ID",bg="#142E54",fg="white",font="Lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    portfolio_id.grid(row=0,column=1,sticky=N+E+W+S)

    name = Label(Pycripto,text="Coin Name",bg="#142E54",fg="white",font="Lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    name.grid(row=0,column=2,sticky=N+E+W+S)

    price = Label(Pycripto,text="Price",bg="#142E54",fg="white",font="Lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    price.grid(row=0,column=3,sticky=N+E+W+S)

    no_coins = Label(Pycripto,text="Coins Owned",bg="#142E54",fg="white",font="Lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    no_coins.grid(row=0,column=4,sticky=N+E+W+S)

    total_paid = Label(Pycripto,text="Paid Amount",bg="#142E54",fg="white",font="Lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    total_paid.grid(row=0,column=5,sticky=N+E+W+S)

    current_price = Label(Pycripto,text="Current Price",bg="#142E54",fg="white",font="Lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    current_price.grid(row=0,column=6,sticky=N+E+W+S)

    PL_per_coin = Label(Pycripto,text="P/L per coin",bg="#142E54",fg="white",font="Lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    PL_per_coin.grid(row=0,column=7,sticky=N+E+W+S)

    total_pl_coin = Label(Pycripto,text="Total PL with Coin",bg="#142E54",fg="white",font="Lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    total_pl_coin.grid(row=0,column=8,sticky=N+E+W+S)

app_nav()
app_header()
myPorfolio()
Pycripto.mainloop()

curobj.close()
con.close()

print("Program Completed")