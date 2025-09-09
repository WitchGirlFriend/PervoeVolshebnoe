import datetime
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showwarning
import tkcalendar
import reportlab
import babel.numbers
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.platypus.tables import Table, TableStyle
from reportlab.platypus import Paragraph

import pyodbc as sql
from datetime import date
from tkinter import messagebox

from reportlab.platypus import PageBreak

con = sql.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=[redacted];DATABASE=model;Trusted_Connection=yes;")
cur = con.cursor()
cur2 = con.cursor()


def counting_price(order_content):
    global content
    orders = content
    temp = []
    for i in orders:
        cur.execute(f"SELECT req_price from requisite WHERE req_id = {i}")
        pr = cur.fetchall()
        temp.append(int(pr[0][0]))
    a = sum(temp)
    return a

def creating_contract(cl_id, order_content, date_return, pay):
    global c
    month = date.today().month
    print_month = ''
    print_return = ''
    g = (f"{date_return}".split('/'))
    day_return = g[1]
    month_return = g[0]
    year_return = g[2]
    cur.execute(f"SELECT cl_phone from client where cl_name = '{cl_id}'")
    phone = cur.fetchone()[0]
    cur.execute(f"SELECT cl_address from client where cl_name = '{cl_id}'")
    address = cur.fetchone()[0]
    match month:
        case 1:
            print_month = "января"
        case 2:
            print_month = "февраля"
        case 3:
            print_month = "марта"
        case 4:
            print_month = "апреля"
        case 5:
            print_month = "мая"
        case 6:
            print_month = "июня"
        case 7:
            print_month = "июля"
        case 8:
            print_month = "августа"
        case 9:
            print_month = "сентября"
        case 10:
            print_month = "октября"
        case 11:
            print_month = "ноября"
        case 12:
            print_month = "декабря"

    match month_return:
        case '1':
            print_return = "января"
        case '2':
            print_return = "февраля"
        case '3':
            print_return = "марта"
        case '4':
            print_return = "апреля"
        case '5':
            print_return = "мая"
        case '6':
            print_return = "июня"
        case '7':
            print_return = "июля"
        case '8':
            print_return = "августа"
        case '9':
            print_return = "сентября"
        case '10':
            print_return = "октября"
        case '11':
            print_return = "ноября"
        case '12':
            print_return = "декабря"
    cur.execute(f"SELECT cl_address from client WHERE cl_name = '{cl_id}'")
    address = cur.fetchone()[0]
    price = counting_price(order_content)
    fileName = f'order-{c}.pdf'
    documentTitle = f"Договор №{c}"
    title = f"ДОГОВОР №{c}"
    subTitle = 'проката костюмов, ростовых кукол, аксессуаров, декораций, бутафории и реквизита.'
    textLines = [
        f'г. Тюмень                                                                                                      «{date.today().day}» {print_month} {date.today().year} год',
        'Общество с ограниченной ответственностью «Мэйджик», именуемое в дальнейшем, Арендодатель, в',
        'лице генерального директора Ершова Ивана Васильевича, действующего на основании Устава, и',
        f'{cl_id} с другой стороны, именуемый в дальнейшем Арендатор, именуемые в',
        'дальнейшем «Стороны», заключили настоящий договор (далее - Договор) о нижеследующем:',
    ]
    pdf = canvas.Canvas(fileName)
    pdf.setTitle(documentTitle)
    pdfmetrics.registerFont(TTFont('tnr', 'times.ttf', 'UTF-8'))
    pdfmetrics.registerFont(TTFont('tnrb', 'timesbd.ttf', 'UTF-8'))
    pdfmetrics.registerFont(TTFont('tnri', 'timesi.ttf', 'UTF-8'))
    pdf.setFont('tnrb', 11)
    pdf.drawCentredString(300, 800, title)
    pdf.setFont('tnri', 11)
    pdf.drawCentredString(290, 780, subTitle)
    text = pdf.beginText(40, 760)
    text.setFont("tnr", 11)
    for line in textLines:
        text.textLine(line)
    pdf.drawText(text)
    pdf.setFont('tnrb', 11)
    title2 = "1. ПРЕДМЕТ ДОГОВОРА"
    pdf.drawCentredString(290, 680, title2)
    pdf.setFont('tnr', 11)
    text2 = pdf.beginText(40, 670)
    subtitle2 = ["1.1 Арендодатель обязуется предоставить Арендатору за плату во временное владение и пользование",
                 "следующие декорации, бутафории, реквизит, аксессуары, ростовые куклы и костюмы, находящиеся в",
                 "полной комплектации: "]
    for z in subtitle2:
        text2.textLine(z)
    text2.setFont("tnr", 11)
    pdf.drawText(text2)
    pdf.setFont('tnrb', 11)
    subtitle3 = f"1.2 {order_content}"
    pdf.drawCentredString(137, 620, subtitle3)
    pdf.setFont("tnr", 11)
    text3 = pdf.beginText(40, 610)
    subtitle4 = ["1.3 Стоимость предмета проката, в случае утери или порчи,  предоставленных по Договору, составляет",
                 f" _____ рублей.",
                 "1.4 Исправность, комплектность и состояние предмета проката проверена в присутствии Арендатора.",
                 "1.5 Арендодатель знакомит Арендатора с правилами эксплуатации технически сложных предметов или",
                 "выдает инструкцию о пользовании ими."]
    for x in subtitle4:
        text3.textLine(x)
    text3.setFont("tnr", 11)
    pdf.drawText(text3)
    pdf.setFont('tnrb', 11)
    title3 = "2. БРОНИРОВАНИЕ, АРЕНДНАЯ ПЛАТА"
    pdf.drawCentredString(290, 520, title3)
    text4 = pdf.beginText(40, 510)
    subtitle5 = [
        f"2.1. За пользование декорациями, предоставленными по настоящему Договору, Арендатор оплачивает {price}",
        "руб.00 к.",
        "2.1.1. Обязательство по возврату предмета проката в надлежащем состоянии может быть обеспечено",
        "залогом (п. 1 ст. 329 ГК РФ). В силу залога Арендодатель имеет право в случае неисполнения",
        "Арендатором такого обязательства получить удовлетворение из стоимости переданного в прокат",
        "имущества. Залог возникает в силу договора (п. п. 1, 3 ст. 334 ГК РФ). Сумма принятого залога",
        f"Арендодателем у Арендатора составляет ____ руб ",
        "2.1.2.Для передаваемого товара в аренду существует система бронирования.Сумма бронирования составляет",
        "__нет___ Сумма бронирования оплачивается предварительно и входит в стоимость проката.В случае отмены",
        "проката сумма брони не возвращается.",
        "2.2.Форма оплаты наличными в кассу Арендодателя в момент передачи предмета.",
        "2.3.В случае несвоевременного возврата предмета проката Арендатором Арендодатель начисляет ему",
        "соответствующую часть арендной платы, исчисляя ее со дня, следующего за днем оговоренного возврата",
        "предмета проката, исходя из утвержденных тарифов Арендодателя.",
        "2.4.Взыскание с Арендатора задолженности по арендной плате производится в бесспорном порядке."
        ]
    text4.setFont("tnr", 11)
    for c in subtitle5:
        text4.textLine(c)
    pdf.drawText(text4)
    pdf.setFont('tnrb', 11)
    title4 = "3. СРОКИ ИСПОЛНЕНИЯ ОБЯЗАТЕЛЬСТВ"
    pdf.drawCentredString(290, 280, title4)
    text5 = pdf.beginText(40, 270)
    subtitle6 = [
        f"3.1. Указанные в п. 1.1 настоящего Договора декорации переданы Арендатору в момент заключения Договора,",
        "Арендатор претензий не имеет.",
        f"3.2. Предмет проката передается Арендатору на срок с «{date.today().day}» {print_month} {date.today().year}г. по «{day_return}» {print_return} {year_return}г.",
        "Время сдачи Предмета проката с 12ч.00 мин до 19ч.00 мин по адресу г.Тюмень, ул. ",
        "Тульская,4, Первое волшебное объединение.",
        "3.3. Настоящий Договор может быть продлен по желанию Арендатора. О продлении Договора Арендатор ",
        f"обязан сообщить Арендодателю в его рабочее время не позднее, чем за четыре часа до окончания срока его",
        "действия.",
        "3.4. Арендатор вправе отказаться от Договора проката в любое время.",
        "3.5. Возврат Арендатором Арендодателю предмета прокатаможет быть осуществлен по акту возврата ",
        "предмета проката."
    ]
    text5.setFont("tnr", 11)
    for v in subtitle6:
        text5.textLine(v)
    pdf.drawText(text5)
    pdf.setFont('tnrb', 11)
    title5 = "4. ОБЯЗАТЕЛЬСТВА СТОРОН"
    pdf.drawCentredString(290, 110, title5)
    text6_5 = pdf.beginText(40, 100)
    subsubtitle7 = [
        "4.1. Арендодатель обязан в присутствии Арендатора проверить исправность предоставленных по Договору",
        "предметов проката, а также ознакомить Арендатора с правилами эксплуатации предмета проката ",
        "либо выдать",
        "ему письменные инструкции о пользовании этими предметами проката."]
    text6_5.setFont("tnr", 11)
    for b in subsubtitle7:
        text6_5.textLine(b)
    pdf.drawText(text6_5)
    text6 = pdf.beginText(40, 800)
    subtitle7 = [
        "4.2. При обнаружении недостатков предоставленных в прокат предметов проката, полностью или частично ",
        "препятствующих пользованию ими, Арендодатель обязан в трехдневный срок со дня заявления Арендатора о ",
        "недостатках безвозмездно устранить недостатки предметов проката на месте либо произвести замену данных ",
        "предметов проката другими, находящимися в надлежащем состоянии, либо Арендодатель",
        "вправе использовать залог Арендатора для оплаты ремонта и транспортировки предметов проката.",
        "4.3. Если недостатки предметов проката явились следствием нарушения Арендатором правил эксплуатации и ",
        "содержания предмета проката и Арендодатель посчитает возможным отремонтировать и исправить такие ",
        "недостатки, Арендатор оплачивает Арендодателю стоимость ремонта и транспортировки предметов проката. ",
        "При этом ремонт предметов проката Арендодатель вправе осуществить как своими силами, так и с помощью ",
        "специализированных мастерских по ремонту либо иных организаций, оказывающих соответствующие услуги.",
        "4.4. В случае утери или порчи предмета проката Арендатор обязуется возместить полную стоимость предмета ",
        "проката согласно п. 1.2 настоящего Договора.",
        "4.5. Капитальный и текущий ремонт предметов проката, сданных в аренду по Договору проката, является ",
        "обязанностью Арендодателя.",
    ]
    pdf.showPage()
    text6.setFont("tnr", 11)
    for b in subtitle7:
        text6.textLine(b)
    pdf.drawText(text6)
    pdf.setFont('tnrb', 11)
    title6 = "5. ОТВЕТСТВЕННОСТЬ СТОРОН И ПОРЯДОК РАЗРЕШЕНИЙ СПОРОВ"
    pdf.drawCentredString(290, 590, title6)
    text7 = pdf.beginText(40, 580)
    subtitle8 = [
        "5.1. За просрочку возврата предмета проката, переданного по настоящему Договору, Арендодатель вправе",
        "потребовать от Арендатора уплаты денежной суммы эквивалентной стоимости предмета проката за ",
        "просроченный период, исходя из утвержденных тарифов и стоимости этой услуги, определенной Договором.",
        "5.2. Все споры или разногласия, возникающие между сторонами по настоящему Договору или в связи с ним, ",
        "разрешаются путем переговоров между сторонами.",
        "5.3. В случае невозможности разрешения разногласий путем переговоров они подлежат рассмотрению в суде ",
        "в установленном законодательством порядке."
    ]
    text7.setFont("tnr", 11)
    for b in subtitle8:
        text7.textLine(b)
    pdf.drawText(text7)
    pdf.setFont('tnrb', 11)
    title7 = "6. ПОРЯДОК ИЗМЕНЕНИЯ И ДОПОЛНЕНИЯ ДОГОВОРА"
    pdf.drawCentredString(290, 480, title7)
    text8 = pdf.beginText(40, 470)
    subtitle9 = [
        "6.1.Любые изменения и дополнения к настоящему Договору проката имеют силу только в том случае, если",
        "они оформлены в письменном виде и подписаны обеими сторонами.",
        "6.2.Арендодатель может требовать досрочного расторжения настоящего Договора в следующих случаях:",
        "  - если Арендатор пользуется редметами проката не в соответствии с настоящим Договором или",
        "назначением предмета проката;",
        "  - если Арендатор умышленно или по неосторожности ухудшает состояние предмета проката;"
    ]
    text8.setFont("tnr", 11)
    for b in subtitle9:
        text8.textLine(b)
    pdf.drawText(text8)
    pdf.setFont('tnrb', 11)
    title8 = "7. ПРОЧИЕ УСЛОВИЯ"
    pdf.drawCentredString(290, 380, title8)
    text9 = pdf.beginText(40, 370)
    subtitle10 = [
        "7.1.Настоящий Договор составлен в двух экземплярах, имеющих одинаковую юридическую силу, по одному",
        "экземпляру для каждой из сторон.",
        f"Договор вступает в силу с {date.today().day} {print_month} {date.today().year}.",
        "7.2.Сдача в субаренду предмета проката, предоставленных Арендатору по настоящему Договору, передача им",
        "своих прав и обязанностей по Договору проката другому лицу, предоставление этого предмета проката в",
        "безвозмездное пользование, залог арендных прав и внесение его в качестве имущественного вклада в",
        "хозяйственные товарищества и общества или паевого взноса в производственные кооперативы, не",
        "допускаются.",
        "7.3.Доставка предмета проката Арендатору и обратно производится Арендатором.При наличии у",
        "Арендодателя транспортных средств доставка предмета проката может производится по желанию Арендатора",
        "Арендодателем и оплачивается Арендатором по установленным тарифам.",
    ]
    text9.setFont("tnr", 11)
    for b in subtitle10:
        text9.textLine(b)
    pdf.drawText(text9)
    title9 = "8. АДРЕСА И БАНКОВСКИЕ РЕКВИЗИТЫ СТОРОН"
    pdf.drawCentredString(290, 220, title9)
    styles = getSampleStyleSheet()
    p = ' '
    if len(cl_id.split(' ')) == 3:
        surname = cl_id.split(' ')[0]
        name = cl_id.split(' ')[1]
        n = name[0]
        patronymic = cl_id.split(' ')[2][0]
        p = f"{patronymic[0]}."
    else:
        surname = cl_id.split(' ')[0]
        name = cl_id.split(' ')[1]
        n = name[0]
    styles["Normal"].fontName = 'tnr'
    styleN = styles["Normal"]
    styleN.wordWrap = "CJK"
    text_last_1 = pdf.beginText(40, 200)
    wr1 = ["              Арендодатель",
           "              ООО «Мэджик»",
           "           redacted"]
    text_last_1.setFont("tnr", 11)
    for b in wr1:
        text_last_1.textLine(b)
    pdf.drawText(text_last_1)
    text_last_2 = pdf.beginText(350, 200)
    wr2 = ["             Арендодатор",
           f"       {surname} {n}.{p}",
           f"      Телефон: {phone}",
           " ",
           "                 Залог:",
           "       Адрес проживания:",
           f"         {address}",
           " ",
           " ",
           "подпись____________________"]
    text_last_2.setFont("tnr", 11)
    for b in wr2:
        text_last_2.textLine(b)
    pdf.drawText(text_last_2)

    pdf.save()


def register_order(cl_id, order_content, date_return, pay, createwin):
    global uncomplete_check, content, c
    c = 0
    if cl_id == '' or order_content == '' or date_return == '' or pay == "":
        showwarning(title="Ошибка", message="Вы заполнили не все данные")
    else:
        date_give = date.today().strftime('%d-%m-%Y')
        price = counting_price(order_content)
        cur2.execute(f"SELECT cl_id from client WHERE cl_name LIKE '{cl_id}'")
        clients_id = cur2.fetchone()
        client = clients_id[0]
        g = (f"{date_return}".split('/'))
        if int(g[0]) < 10:
            g = '-'.join(f"{date_return}".split('/'))
            g = '0' + f'{g}'
        else:
            g = '-'.join(f"{date_return}".split('/'))
        gg = datetime.datetime.strptime(g, "%m-%d-%y")
        gg = gg.strftime("%d-%m-%Y")
        object_list = ""
        for i in content:
            if object_list == "":
                object_list = object_list + f"{i}"
            else:
                object_list = object_list + f", {i}"
        cur2.execute(f"SELECT pay_id from payment WHERE pay_name LIKE '{pay}'")
        payment = cur2.fetchone()
        paying = payment[0]
        if uncomplete_check == "Да":
            uncompleted = "Да"
        else:
            uncompleted = "Нет"

        try:
            cur.execute(
                f"INSERT INTO orders (ord_client, ord_costumes, ord_booked, ord_date_give, ord_date_return, ord_price, ord_payment, ord_uncomplete) VALUES ({client}, '{content}', 2, '{date_give}', '{gg}', {price}, {paying}, '{uncompleted}')")
            con.commit()

            try:
                cur2.execute(
                    f"SELECT ord_id FROM orders WHERE ord_client = {client} and ord_costumes = '{content}' and ord_date_give = '{date_give}'")
                c = cur2.fetchone()[0]
                print(c)
                for i in content:
                    print(i)
                    cur2.execute(f"INSERT INTO order_content (oc_order, oc_content) VALUES ({c}, {i})")
                    con.commit()
                createwin.destroy()
            except:
                showwarning(message="Не удалось внести данные в таблицу oc")
        except:
            showwarning(title="Ошибка", message="Не удалось отправить запрос")
        creating_contract(cl_id, order_content, date_return, pay)


def sort_color():
    global tree, sel_color
    tree.delete(*tree.get_children())
    print(sel_color.get())
    got = sel_color.get()
    cur.execute(f"SELECT col_id from colors WHERE col_name = {got}")
    color = cur.fetchone()
    cur.execute(
        f"SELECT req_id, req_name, colors.col_name, materials.mat_name, req_price, booked.book_name, req_date_give, req_date_return FROM requisite JOIN materials ON requisite.req_mat=materials.mat_id JOIN colors ON requisite.req_col=colors.col_id JOIN booked ON requisite.req_booked=booked WHERE requisite.req_col = {color}")
    costume = cur.fetchall()
    words = []
    for req in get_costumes():
        words.clear()
        for i in req:
            words.append(i)
        tree.insert("", END, values=words)


def get_colors():
    cur2.execute("SELECT col_name FROM colors")
    ta = cur2.fetchall()
    words = []
    for i in ta:
        words.append(i[0])
    return words


def get_materials():
    cur2.execute("SELECT mat_name FROM materials")
    ta = cur2.fetchall()
    words = []
    for i in ta:
        words.append(i[0])
    return words


def get_latest_orders():
    cur.execute(
        f"SELECT * from orders")
    r = cur.fetchall()
    return r


def get_clients():
    cur.execute(
        "SELECT client.cl_id, client.cl_name, client.cl_phone, client.cl_address, client.cl_birthday, client.cl_snils, client.cl_stud, prof.pro_name, client.cl_link FROM client JOIN prof ON client.cl_pro=prof.pro_id")
    f = cur.fetchall()
    fa = []
    for i in range(len(f)):
        fa.append(f[i])
    return fa


def get_booked():
    cur.execute(
        f"SELECT req_id, req_name, colors.col_name, materials.mat_name, req_price, booked.book_name, req_date_give, req_date_return FROM requisite JOIN materials ON requisite.req_mat=materials.mat_id JOIN colors ON requisite.req_col=colors.col_id JOIN booked ON requisite.req_booked=booked.book_id WHERE req_booked = 1")
    r = cur.fetchall()
    fa = []
    for i in range(len(r)):
        fa.append(r[i])
    return fa


def get_book():
    cur.execute(f"SELECT book_name FROM booked")
    r = cur.fetchall()
    words = []
    for i in r:
        words.append(i[0])
    return words


def get_costumes():
    cur.execute(
        f"SELECT req_id, req_name, colors.col_name, materials.mat_name, req_price, booked.book_name, req_date_give, req_date_return FROM requisite JOIN materials ON requisite.req_mat=materials.mat_id JOIN colors ON requisite.req_col=colors.col_id JOIN booked ON requisite.req_booked=booked.book_id")
    r = cur.fetchall()
    return r


def get_frequent():
    global treev
    treev.delete(*treev.get_children())
    cur2.execute(
        "SELECT client.cl_id, COUNT(orders.ord_client) As TotalCount FROM client LEFT JOIN orders ON client.cl_id = orders.ord_client GROUP BY client.cl_id ORDER BY TotalCount DESC")
    a = cur2.fetchall()
    ids = []
    for i in a:
        ids.append(i[0])
    for k in ids:
        people = []
        cur.execute(
            f"SELECT client.cl_id, client.cl_name, client.cl_address, client.cl_birthday, client.cl_snils, client.cl_stud, prof.pro_name, client.cl_link FROM client JOIN prof ON client.cl_pro=prof.pro_id WHERE cl_id IN ({k})")
        b = cur.fetchone()
        for z in b:
            people.append(z)
        treev.insert("", END, values=people)


def get_job():
    global treev, cl_search
    treev.delete(*treev.get_children())
    if cl_search.get() == '' or cl_search.get() == " ":
        cur2.execute(
            f"SELECT client.cl_id, client.cl_name, client.cl_address, client.cl_birthday, client.cl_snils, client.cl_stud, prof.pro_name, client.cl_link FROM client JOIN prof ON client.cl_pro=prof.pro_id WHERE cl_pro BETWEEN 2 AND 3")
        t = cur2.fetchall()
        ta = []
        for i in t:
            ta.clear()
            for z in i:
                ta.append(z)
            treev.insert("", END, values=ta)
    else:
        cur2.execute(
            f"SELECT client.cl_id, client.cl_name, client.cl_address, client.cl_birthday, client.cl_snils, client.cl_stud, prof.pro_name, client.cl_link FROM client JOIN prof ON client.cl_pro=prof.pro_id WHERE cl_pro BETWEEN 2 AND 3 AND cl_name LIKE '%{cl_search.get()}%' ")
        t = cur2.fetchall()
        ta = []
        for i in t:
            ta.clear()
            for z in i:
                ta.append(z)
            treev.insert("", END, values=ta)
    pass


def get_payments():
    cur.execute("SELECT pay_name from payment")
    h = cur.fetchall()
    ta = []
    for i in h:
        ta.append(i[0])
    return ta


def refresh_clients():
    global treev, cl_search
    treev.delete(*treev.get_children())
    if cl_search.get() == '' or cl_search.get() == " ":
        treev.delete(*treev.get_children())
        got_clients = get_clients()
        words = []
        for req in got_clients:
            words.clear()
            for i in req:
                words.append(i)
            treev.insert("", END, values=words)
    else:
        cur.execute(
            f"SELECT client.cl_id, client.cl_name, client.cl_address, client.cl_birthday, client.cl_snils, client.cl_stud, prof.pro_name, client.cl_link FROM client JOIN prof ON client.cl_pro=prof.pro_id WHERE cl_name LIKE '%{cl_search.get()}%'")
        a = cur.fetchall()
        words = []
        for req in a:
            words.clear()
            for i in req:
                words.append(i)
            treev.insert("", END, values=words)


def get_birthdays():
    global treev, cl_search
    treev.delete(*treev.get_children())
    s = date.today().strftime('%d-%m-%Y')
    if cl_search.get() == '' or cl_search.get() == " ":
        cur2.execute(
            f"SELECT client.cl_id, client.cl_name, client.cl_address, client.cl_birthday, client.cl_snils, client.cl_stud, prof.pro_name, client.cl_link FROM client JOIN prof ON client.cl_pro=prof.pro_id WHERE cl_birthday = '{s}'")
        t = cur2.fetchall()
        ta = []
        for i in t:
            ta.clear()
            for z in i:
                ta.append(z)
            treev.insert("", END, values=ta)
    else:
        cur2.execute(
            f"SELECT client.cl_id, client.cl_name, client.cl_address, client.cl_birthday, client.cl_snils, client.cl_stud, prof.pro_name, client.cl_link FROM client JOIN prof ON client.cl_pro=prof.pro_id WHERE cl_birthday = '{s}' AND cl_name LIKE '%{cl_search.get()}%' ")
        t = cur2.fetchall()
        ta = []
        for i in t:
            ta.clear()
            for z in i:
                ta.append(z)
            treev.insert("", END, values=ta)


def uncomplete(signal):
    global uncomplete_check
    uncomplete_check = "Нет"
    if signal == "yes":
        uncomplete_check = "Да"


def add_to_order(combo, labl):
    global line, content
    got = combo
    if got not in line:
        cur.execute(f"SELECT req_id from requisite WHERE req_name = '{got}'")
        f = cur.fetchone()[0]
        content.append(f)
        if line == '':
            line = f"{got}"
        else:
            line = f"{line}, {got}"
    labl["text"] = f"{line}"


def create():
    global tree, line, content
    createwin = tk.Tk()
    createwin.minsize(1820, 720)
    createwin.maxsize(1820, 720)
    cl_btn = tk.Button(createwin, text="Добавить клиента", command=clients)
    cl_btn.pack()
    uncomplete("no")
    fr = tk.Frame(createwin)
    fr.pack(pady=20)
    tk.Label(fr, text="КЛИЕНТ").pack(pady=20)
    cur.execute("SELECT cl_name FROM client")
    c = cur.fetchall()
    ta = []
    for i in c:
        ta.append(i[0])
    client = ttk.Combobox(fr)
    client.pack(side="top", pady=10)
    client["values"] = ta
    cur2.execute("SELECT req_name FROM requisite")
    co = cur2.fetchall()
    ca = []
    for i in co:
        ca.append(i[0])
    tk.Label(fr, text="КОСТЮМ").pack(pady=20)
    costumes = ttk.Combobox(fr)
    costumes.pack(side="top", pady=10)
    costumes["values"] = ca
    line = ""
    content = []
    add_costume = tk.Button(fr, text="Добавить в заказ", command=lambda: add_to_order(costumes.get(), requisites))
    add_costume.pack(side="top", pady=20)
    requisites = tk.Label(fr)
    requisites.pack(padx=50)
    ncompl = tk.Button(fr, text="Раскомплектовать", command=lambda: uncomplete("yes"))
    ncompl.pack(padx=50)
    tk.Label(fr, text="ДАТА ВОЗВРАЩЕНИЯ").pack(side="top", pady=20)
    giv_date = tkcalendar.DateEntry(fr, width=12, background='darkblue', foreground='white',
                                    borderwidth=2)
    giv_date.pack(side="top", padx=10, pady=10)
    pay = ttk.Combobox(fr)
    tk.Label(fr, text="СПОСОБ ОПЛАТЫ").pack(side="top", pady=20)
    pay.pack(side="top", pady=10)
    payments = get_payments()
    pay["values"] = payments
    cr_ord = tk.Button(fr, text="Создать заказ",
                       command=lambda: register_order(client.get(), requisites.cget("text"), giv_date.get(), pay.get(),
                                                      createwin))
    cr_ord.pack(side="top", pady=20)
    createwin.mainloop()


def clients():
    global treev, cl_search
    clientswin = tk.Tk()
    clientswin.minsize(1820, 720)
    clientswin.maxsize(1280, 780)
    add_cl = tk.Button(clientswin, text="Добавить клиента", command=add_clients)
    add_cl.pack(side="top")
    column = ["id", "name", "phone", "address", "birthday", "snils", "stud", "prof", "link"]
    treev = ttk.Treeview(clientswin, columns=column, show="headings")
    treev.pack(fill=BOTH, expand=1, pady=40)
    treev.heading("id", text="№ п/п")
    treev.heading("name", text="ФИО")
    treev.heading("phone", text="Телефон")
    treev.heading("address", text="Адрес")
    treev.heading("birthday", text="Дата рождения")
    treev.heading("snils", text="СНИЛС")
    treev.heading("stud", text="Студенческий")
    treev.heading("prof", text="Профессия")
    treev.heading("link", text="Ссылка")
    got_clients = get_clients()
    words = []
    for req in got_clients:
        words.clear()
        for i in req:
            words.append(i)
        treev.insert("", END, values=words)
    treev.bind("<<TreeviewSelect>>", item_selected)

    searching = StringVar()
    cl_search = tk.Entry(clientswin, textvariable=searching)
    cl_search.pack(side="left", padx=50, pady=20)

    bd = tk.Button(clientswin, text="ДР", command=get_birthdays)
    bd.pack(side="left", padx=50, pady=20)
    freq = tk.Button(clientswin, text="Частый", command=get_frequent)
    freq.pack(side="left", padx=50, pady=20)
    job = tk.Button(clientswin, text="Артист", command=get_job)
    job.pack(side="left", padx=50, pady=20)
    res = tk.Button(clientswin, text="Сброс", command=refresh_clients)
    res.pack(side="left", padx=50, pady=20)


def SearchClient(*args):
    Keyword = search.get()
    cur.execute(f"SELECT * FROM client JOIN profile ON client.cl_pro=profile.pro_id WHERE cl_name LIKE '%{Keyword}%'")


def send_new_client(name, phone, adress, bday, snils, stud, pro, link):
    global clientswin
    clientswin.destroy()

    cur2.execute(f"SELECT pro_id from prof WHERE pro_name = '{pro}'")
    j = cur2.fetchone()
    try:
        cur.execute(
            f"INSERT INTO client (cl_name, cl_phone, cl_address, cl_birthday, cl_snils, cl_stud, cl_pro, cl_link) VALUES ('{name}', '{phone}', '{adress}', '{bday}', '{snils}', '{stud}', '{j[0]}', '{link}')")
        con.commit()
    except:
        showwarning(title="Ошибка", message="Что-то пошло не так, проверьте БД")


def add_clients():
    global tree, clientswin
    clientswin = tk.Tk()
    clientswin.minsize(720, 720)
    clientswin.maxsize(780, 780)
    tk.Label(clientswin, text="ФИО").pack(side="top", pady=10)
    name = tk.Entry(clientswin)
    name.pack(side="top", pady=10)
    tk.Label(clientswin, text="Телефон").pack(side="top", pady=10)
    phone = tk.Entry(clientswin)
    phone.pack(side="top", pady=10)
    tk.Label(clientswin, text="Адрес").pack(side="top", pady=10)
    adress = tk.Entry(clientswin)
    adress.pack(side="top", pady=10)
    tk.Label(clientswin, text="Дата рождения (дд-мм-гггг)").pack(side="top", pady=10)
    bd = tk.Entry(clientswin)
    bd.pack(side="top", pady=10)
    tk.Label(clientswin, text="СНИЛС (необязательно)").pack(side="top", pady=10)
    snils = tk.Entry(clientswin)
    snils.pack(side="top", pady=10)
    tk.Label(clientswin, text="Студенческий (необязательно)").pack(side="top", pady=10)
    stud = tk.Entry(clientswin)
    stud.pack(side="top", pady=10)
    tk.Label(clientswin, text="Профессия").pack(side="top", pady=10)

    cur2.execute("SELECT * FROM prof")
    z = cur2.fetchall()
    profs = []
    for i in z:
        profs.append(i[1])

    pro = ttk.Combobox(clientswin)
    pro.pack(side="top", pady=10)

    pro["values"] = profs
    pro["state"] = 'readonly'
    pro.set("Нет")
    tk.Label(text="Ссылка").pack(side="top", pady=10)
    link = tk.Entry(clientswin)
    link.pack(side="top", pady=10)
    add = tk.Button(clientswin, text="Добавить клиента",
                    command=lambda: send_new_client(name.get(), phone.get(), adress.get(), bd.get(), snils.get(),
                                                    stud.get(), pro.get(), link.get()))
    add.pack(side="top", pady=10)


def booked():
    global tree
    bookwin = tk.Tk()
    bookwin.minsize(1820, 720)
    bookwin.maxsize(1820, 720)
    book_btn = tk.Button(bookwin, text="Брони", command=get_book)
    book_btn.pack()
    column = ["id", "name", "color", "material", "price", "booked", "date_give", "date_return"]
    tree = ttk.Treeview(bookwin, columns=column, show="headings")
    tree.pack(fill=BOTH, expand=1)
    tree.heading("id", text="№ п/п")
    tree.heading("name", text="Наименование")
    tree.heading("color", text="Цвет")
    tree.heading("material", text="Материал")
    tree.heading("price", text="Цена")
    tree.heading("booked", text="Бронь")
    tree.heading("date_give", text="Дата выдачи")
    tree.heading("date_return", text="Дата возврата")
    got_booked = get_booked()
    words = []
    for req in got_booked:
        words.clear()
        for i in req:
            words.append(i)
        tree.insert("", END, values=words)
    tree.bind("<<TreeviewSelect>>", item_selected)

    refresh_btn = tk.Button(bookwin, text="Обновить", command=refresh_booked)
    refresh_btn.pack()


def get_costume_analized():
    cur.execute(
        "SELECT requisite.req_name,COUNT(*) as cout FROM order_content JOIN requisite ON order_content.oc_content = requisite.req_id GROUP BY requisite.req_name ORDER BY cout DESC;")
    a = cur.fetchall()
    return a


def analise_costume():
    ac = tk.Tk()
    ac.minsize(720, 720)
    ac.maxsize(720, 720)
    column = ["id", "name"]
    treec = ttk.Treeview(ac, columns=column, show="headings")
    treec.pack(fill=BOTH, expand=1, pady=40)
    treec.heading("id", text="Наименование")
    treec.heading("name", text="Количество заказов")
    words = []
    for req in get_costume_analized():
        words.clear()
        for i in req:
            words.append(i)
        treec.insert("", END, values=words)
    treec.bind("<<TreeviewSelect>>", item_selected)
    ac.mainloop()


def analise_client():
    cur2.execute(
        "SELECT orders.ord_client, client.cl_name, COUNT(*) as cout from orders LEFT JOIN client ON orders.ord_client = client.cl_id GROUP BY ord_client, cl_name ORDER BY cout DESC")
    getem = cur2.fetchall()
    acl = tk.Tk()
    acl.minsize(720, 720)
    acl.maxsize(720, 720)
    column = ["id", "name", "freq"]
    treec = ttk.Treeview(acl, columns=column, show="headings")
    treec.pack(fill=BOTH, expand=1, pady=40)
    treec.heading("id", text="Идентификатор заказчика")
    treec.heading("name", text="ФИО заказчика")
    treec.heading("freq", text="Количество заказов")
    words = []
    for req in getem:
        words.clear()
        for i in req:
            words.append(i)
        treec.insert("", END, values=words)
    treec.bind("<<TreeviewSelect>>", item_selected)
    acl.mainloop()


def analise_shift():
    acl = tk.Tk()
    acl.minsize(720, 720)
    acl.maxsize(720, 720)
    date_give = date.today().strftime('%d-%m-%Y')
    date_give = '13-08-2024'
    try:
        cur2.execute(f"SELECT COUNT(*) FROM orders WHERE ord_date_give = '{date_give}'")
        getem = cur2.fetchone()[0]
    except:
        showwarning(message="Не хватает данных о заказах для аналитики!")
        getem = 0

    lab = tk.Label(acl, text=f"За сегодня было совершено {getem} заказ(ов)")
    lab.pack()
    try:
        cur.execute(
            f"select TOP 1 ord_payment, count(*) as count from orders WHERE ord_date_give = '{date_give}' group by ord_payment ORDER BY ord_payment DESC;")
        z = cur.fetchone()[0]
        cur2.execute(f"SELECT pay_name from payment WHERE pay_id = {z}")
        v = cur2.fetchone()[0]
    except:
        showwarning(message="Не хватает данных об оплатах для аналитики!")
        v = 'Неизвестно'
    lab2 = tk.Label(acl, text=f"Чаще всего оплата была посредством: {v}")
    lab2.pack()
    try:
        cur.execute(
            f"SELECT payment.pay_name, SUM(ord_price) as summ FROM orders JOIN payment ON ord_payment = pay_id WHERE ord_date_give = '{date_give}' GROUP BY pay_name ORDER BY summ DESC")
        whole = cur.fetchall()
        mass = 'Суммарно:\n'
        for i in whole:
            for k in i:
                mass = mass + f"{k} "
            mass = mass + "\n"
    except:
        showwarning(message="Не хватает данных об оплатах для аналитики!")
        mass = "-"
    lab3 = tk.Label(acl, text=mass)
    lab3.pack()
    acl.mainloop()


def analise():
    analize = tk.Tk()
    analize.title("Аналитика")
    analize.minsize(1820, 720)
    analize.maxsize(1820, 720)
    cost = tk.Button(analize, text="По костюму", command=analise_costume)
    cost.pack(pady=30)
    client = tk.Button(analize, text="По клиенту", command=analise_client)
    client.pack(pady=30)
    shift = tk.Button(analize, text="По смене", command=analise_shift)
    shift.pack(pady=30)
    analize.mainloop()


def send_new_info(name, color, material, price):
    cur.execute(f"SELECT col_id from colors WHERE col_name = '{color}'")
    col_id = cur.fetchone()[0]
    cur.execute(f"SELECT mat_id from materials WHERE mat_name = '{material}'")
    mat_id = cur.fetchone()[0]
    try:
        cur2.execute(
            f"INSERT INTO requisite (req_name, req_mat, req_col, req_price, req_booked, req_date_give, req_date_return) VALUES ('{name}', '{mat_id}', '{col_id}', {price}, 2, '-', '-')")
        con.commit()
        showwarning(title="Успех", message="Новый объект добавлен")
    except:
        showwarning(title="Ошибка", message="Что-то пошло не так. Проверьте БД.")


def send_material(m, mtree):
    cur.execute(f"INSERT INTO materials (mat_name) VALUES ('{m}')")
    con.commit()
    mtree.delete(*mtree.get_children())
    cur2.execute("SELECT * FROM materials")
    z = cur2.fetchall()
    words = []
    for req in z:
        words.clear()
        for i in req:
            words.append(i)
        mtree.insert("", END, values=words)


def add_materials():
    mat_scr = tk.Tk()
    mat_scr.title("Добавить материал")
    mat_scr.minsize(700, 700)
    mat_scr.maxsize(900, 900)
    column = ["id", "name"]
    mtree = ttk.Treeview(mat_scr, columns=column, show="headings")
    mtree.pack(fill=BOTH, expand=1)
    mtree.heading("id", text="№ п/п")
    mtree.heading("name", text="Материал")
    cur2.execute("SELECT * FROM materials")
    z = cur2.fetchall()
    words = []
    for req in z:
        words.clear()
        for i in req:
            words.append(i)
        mtree.insert("", END, values=words)
    new_mat = tk.Entry(mat_scr)
    new_mat.pack(anchor="s")
    add = tk.Button(mat_scr, text="Добавить", command=lambda: send_material(new_mat.get(), mtree))
    add.pack(anchor="s")
    mat_scr.mainloop()


def send_color(n, ctree):
    cur.execute(f"INSERT INTO colors (col_name) VALUES ('{n}')")
    con.commit()
    ctree.delete(*ctree.get_children())
    cur2.execute("SELECT * FROM colors")
    z = cur2.fetchall()
    words = []
    for req in z:
        words.clear()
        for i in req:
            words.append(i)
        ctree.insert("", END, values=words)


def add_colors():
    col_scr = tk.Tk()
    col_scr.title("Добавить цвет")
    col_scr.minsize(700, 700)
    col_scr.maxsize(900, 900)
    column = ["id", "name"]
    ctree = ttk.Treeview(col_scr, columns=column, show="headings")
    ctree.pack(fill=BOTH, expand=1)
    ctree.heading("id", text="№ п/п")
    ctree.heading("name", text="Цвет")
    cur2.execute("SELECT * FROM colors")
    z = cur2.fetchall()
    words = []
    for req in z:
        words.clear()
        for i in req:
            words.append(i)
        ctree.insert("", END, values=words)
    new_color = tk.Entry(col_scr)
    new_color.pack(anchor="s")
    add = tk.Button(col_scr, text="Добавить", command=lambda: send_color(new_color.get(), ctree))
    add.pack(anchor="s")
    col_scr.mainloop()


def add_info():
    info = tk.Tk()
    info.title("Добавить реквизит")
    info.minsize(700, 700)
    info.maxsize(900, 900)
    frame_1 = tk.Frame(info)
    frame_1.pack(anchor="s")
    frame_2 = tk.Frame(info)
    frame_2.pack(anchor="w")
    hint = tk.Label(info,
                    text="Это окно нужно закрыть, после того, как добавите новые цвета или материалы, чтобы они отображались").pack()
    add_color = tk.Button(frame_2, text="Добавить цвет", command=add_colors)
    add_color.pack(pady=10)
    add_mat = tk.Button(frame_2, text="Добавить материал", command=add_materials)
    add_mat.pack(pady=10)
    color_values = get_colors()
    material_values = get_materials()
    tk.Label(frame_1, text="Наименование").pack(side="top", pady=10)
    naming = tk.Entry(frame_1)
    naming.pack(pady=20)
    tk.Label(frame_1, text="Цвет").pack(side="top", pady=10)
    coloring = ttk.Combobox(frame_1)
    coloring["values"] = color_values
    coloring.pack(pady=20)
    tk.Label(frame_1, text="Материал").pack(side="top", pady=10)
    materialing = ttk.Combobox(frame_1)
    materialing["values"] = material_values
    materialing.pack(pady=20)
    tk.Label(frame_1, text="Цена").pack(side="top", pady=10)
    pricing = tk.Entry(frame_1)
    pricing.pack(pady=20)
    submit = tk.Button(frame_1, text="Добавить",
                       command=lambda: send_new_info(naming.get(), coloring.get(), materialing.get(), pricing.get()))
    submit.pack()
    info.mainloop()


def admin():
    global tree, color, material, search
    win.destroy()
    root = tk.Tk()
    root.title("Костюмы и реквизит")
    root.minsize(1620, 720)
    root.maxsize(1620, 720)
    frame_1 = tk.Frame(root)
    frame_1.pack(anchor=N)

    book_btn = tk.Button(frame_1, text="Брони", command=booked)
    book_btn.pack(side="left", padx=50)
    order_btn = tk.Button(frame_1, text="Создать заказ\бронь", command=create)
    order_btn.pack(side="left", padx=50)
    client_btn = tk.Button(frame_1, text="Клиенты", command=clients)
    client_btn.pack(side="left", padx=50)
    info_btn = tk.Button(frame_1, text="Данные", command=add_info)
    info_btn.pack(side="left", padx=50)
    analise_btn = tk.Button(frame_1, text="Аналитика", command=analise)
    analise_btn.pack(side="left", padx=50)
    column = ["id", "name", "color", "material", "price", "booked", "date_give", "date_return"]
    tree = ttk.Treeview(root, columns=column, show="headings")
    tree.pack(anchor=CENTER, fill=BOTH, expand=TRUE)
    frame_2 = tk.Frame(root)
    frame_2.pack(anchor=S)
    refresh_btn = tk.Button(frame_2, text="Обновить", command=refresh_admin)
    refresh_btn.pack(side="left", padx=50)

    searching = StringVar()
    search = tk.Entry(frame_2, textvariable=searching)
    search.pack(side="left", padx=50)

    color_values = get_colors()
    material_values = get_materials()

    color = ttk.Combobox(frame_2)
    color['state'] = 'readonly'
    color["values"] = color_values
    color.pack(side="left", padx=50)
    material = ttk.Combobox(frame_2)
    material["values"] = material_values
    material.pack(side="left", padx=50)
    material.set("Не выбрано")
    material['state'] = 'readonly'
    color.set("Не выбрано")

    tree.heading("id", text="№ п/п")
    tree.heading("name", text="Наименование")
    tree.heading("color", text="Цвет")
    tree.heading("material", text="Материал")
    tree.heading("price", text="Цена")
    tree.heading("booked", text="Бронь")
    tree.heading("date_give", text="Дата выдачи")
    tree.heading("date_return", text="Дата возврата")
    tree.tag_configure('red', background='#FF9C9C')
    tree.tag_configure('black', background="#A4A2A2")
    tree.tag_configure('red-black', background="#836262")
    got_costumes = get_costumes()
    words = []
    for req in got_costumes:
        words.clear()
        for i in req:
            words.append(i)
        if words[5] == f"Забронировано" and words[7] != f"{date.today()}":
            tree.insert("", END, values=words, tag='black')
        elif words[5] != f"Забронировано" and words[7] == f"{date.today()}":
            tree.insert("", END, values=words, tag='red')
        elif words[5] == f"Забронировано" and words[7] == f"{date.today()}":
            tree.insert("", END, values=words, tag='red-black')
        else:
            tree.insert("", END, values=words)
    tree.bind("<<TreeviewSelect>>", item_selected)


def refresh_admin():
    global tree, color, material, search
    try:
        for i in tree.selection():
            tree.selection_remove(i)
        tree.delete(*tree.get_children())
        costumes_1 = get_costumes()
        Keyword = search.get()
        if Keyword != '':
            if material.get() == "Не выбрано" and color.get() == "Не выбрано":
                words = []
                cur.execute(
                    f"SELECT req_id, req_name, colors.col_name, materials.mat_name, req_price, booked.book_name, req_date_give, req_date_return FROM requisite JOIN materials ON requisite.req_mat=materials.mat_id JOIN colors ON requisite.req_col=colors.col_id JOIN booked ON requisite.req_booked=booked.book_id WHERE req_name LIKE '%{Keyword}%'")
                costume = cur.fetchall()
                for req in costume:
                    words.clear()
                    for i in req:
                        words.append(i)
                    if words[5] == f"Забронировано" and words[7] != f"{date.today()}":
                        tree.insert("", END, values=words, tag='black')
                    elif words[5] != f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red')
                    elif words[5] == f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red-black')
                    else:
                        tree.insert("", END, values=words)
            if color.get() != "Не выбрано" and material.get() == "Не выбрано":
                a = color.get()
                cur.execute(f"SELECT col_id from colors WHERE col_name = '{a}'")
                colored = cur.fetchone()
                col = colored[0]
                cur.execute(
                    f"SELECT req_id, req_name, colors.col_name, materials.mat_name, req_price, booked.book_name, req_date_give, req_date_return FROM requisite JOIN materials ON requisite.req_mat=materials.mat_id JOIN colors ON requisite.req_col=colors.col_id JOIN booked ON requisite.req_booked=booked.book_id WHERE requisite.req_col = {col} and req_name LIKE '%{Keyword}%'")
                costume = cur.fetchall()
                words = []
                for req in costume:
                    words.clear()
                    for i in req:
                        words.append(i)
                    if words[5] == f"Забронировано" and words[7] != f"{date.today()}":
                        tree.insert("", END, values=words, tag='black')
                    elif words[5] != f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red')
                    elif words[5] == f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red-black')
                    else:
                        tree.insert("", END, values=words)
            if color.get() == "Не выбрано" and material.get() != "Не выбрано":
                a = material.get()
                cur.execute(f"SELECT mat_id from materials WHERE mat_name = '{a}'")
                materia = cur.fetchone()
                mat = materia[0]
                cur.execute(
                    f"SELECT req_id, req_name, colors.col_name, materials.mat_name, req_price, booked.book_name, req_date_give, req_date_return FROM requisite JOIN materials ON requisite.req_mat=materials.mat_id JOIN colors ON requisite.req_col=colors.col_id JOIN booked ON requisite.req_booked=booked.book_id WHERE requisite.req_mat = {mat} and req_name LIKE '%{Keyword}%'")
                costume = cur.fetchall()

                words = []
                for req in costume:
                    words.clear()
                    for i in req:
                        words.append(i)
                    if words[5] == f"Забронировано" and words[7] != f"{date.today()}":
                        tree.insert("", END, values=words, tag='black')
                    elif words[5] != f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red')
                    elif words[5] == f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red-black')
                    else:
                        tree.insert("", END, values=words)
            if color.get() != "Не выбрано" and material.get() != "Не выбрано":
                a = material.get()
                b = color.get()
                cur.execute(f"SELECT mat_id from materials WHERE mat_name = '{a}'")
                materia = cur.fetchone()
                mat = materia[0]
                cur.execute(f"SELECT col_id from colors WHERE col_name = '{b}'")
                colored = cur.fetchone()
                col = colored[0]
                cur.execute(
                    f"SELECT req_id, req_name, colors.col_name, materials.mat_name, req_price, booked.book_name, req_date_give, req_date_return FROM requisite JOIN materials ON requisite.req_mat=materials.mat_id JOIN colors ON requisite.req_col=colors.col_id JOIN booked ON requisite.req_booked=booked.book_id WHERE requisite.req_mat = {mat} and requisite.req_col = {col} and req_name LIKE '%{Keyword}%'")
                costume = cur.fetchall()
                words = []
                for req in costume:
                    words.clear()
                    for i in req:
                        words.append(i)
                    if words[5] == f"Забронировано" and words[7] != f"{date.today()}":
                        tree.insert("", END, values=words, tag='black')
                    elif words[5] != f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red')
                    elif words[5] == f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red-black')
                    else:
                        tree.insert("", END, values=words)
        else:
            if material.get() == "Не выбрано" and color.get() == "Не выбрано":
                words = []
                for req in get_costumes():
                    words.clear()
                    for i in req:
                        words.append(i)
                    if words[5] == f"Забронировано" and words[7] != f"{date.today()}":
                        tree.insert("", END, values=words, tag='black')
                    elif words[5] != f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red')
                    elif words[5] == f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red-black')
                    else:
                        tree.insert("", END, values=words)
            if color.get() != "Не выбрано" and material.get() == "Не выбрано":
                a = color.get()
                cur.execute(f"SELECT col_id from colors WHERE col_name = '{a}'")
                colored = cur.fetchone()
                col = colored[0]
                cur.execute(
                    f"SELECT req_id, req_name, colors.col_name, materials.mat_name, req_price, booked.book_name, req_date_give, req_date_return FROM requisite JOIN materials ON requisite.req_mat=materials.mat_id JOIN colors ON requisite.req_col=colors.col_id JOIN booked ON requisite.req_booked=booked.book_id WHERE requisite.req_col = {col}")
                costume = cur.fetchall()
                words = []
                for req in costume:
                    words.clear()
                    for i in req:
                        words.append(i)
                    if words[5] == f"Забронировано" and words[7] != f"{date.today()}":
                        tree.insert("", END, values=words, tag='black')
                    elif words[5] != f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red')
                    elif words[5] == f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red-black')
                    else:
                        tree.insert("", END, values=words)
            if color.get() == "Не выбрано" and material.get() != "Не выбрано":
                a = material.get()
                cur.execute(f"SELECT mat_id from materials WHERE mat_name = '{a}'")
                materia = cur.fetchone()
                mat = materia[0]
                cur.execute(
                    f"SELECT req_id, req_name, colors.col_name, materials.mat_name, req_price, booked.book_name, req_date_give, req_date_return FROM requisite JOIN materials ON requisite.req_mat=materials.mat_id JOIN colors ON requisite.req_col=colors.col_id JOIN booked ON requisite.req_booked=booked.book_id WHERE requisite.req_mat = {mat}")
                costume = cur.fetchall()
                words = []
                for req in costume:
                    words.clear()
                    for i in req:
                        words.append(i)
                    if words[5] == f"Забронировано" and words[7] != f"{date.today()}":
                        tree.insert("", END, values=words, tag='black')
                    elif words[5] != f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red')
                    elif words[5] == f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red-black')
                    else:
                        tree.insert("", END, values=words)
            if color.get() != "Не выбрано" and material.get() != "Не выбрано":
                a = material.get()
                b = color.get()
                cur.execute(f"SELECT mat_id from materials WHERE mat_name = '{a}'")
                materia = cur.fetchone()
                mat = materia[0]
                cur.execute(f"SELECT col_id from colors WHERE col_name = '{b}'")
                colored = cur.fetchone()
                col = colored[0]
                cur.execute(
                    f"SELECT req_id, req_name, colors.col_name, materials.mat_name, req_price, booked.book_name, req_date_give, req_date_return FROM requisite JOIN materials ON requisite.req_mat=materials.mat_id JOIN colors ON requisite.req_col=colors.col_id JOIN booked ON requisite.req_booked=booked.book_id WHERE requisite.req_mat = {mat} and requisite.req_col = {col}")
                costume = cur.fetchall()
                words = []
                for req in costume:
                    words.clear()
                    for i in req:
                        words.append(i)
                    if words[5] == f"Забронировано" and words[7] != f"{date.today()}":
                        tree.insert("", END, values=words, tag='black')
                    elif words[5] != f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red')
                    elif words[5] == f"Забронировано" and words[7] == f"{date.today()}":
                        tree.insert("", END, values=words, tag='red-black')
                    else:
                        tree.insert("", END, values=words)
    except:
        pass


def refresh_booked():
    global tree
    tree.delete(*tree.get_children())
    words = []
    for req in get_booked():
        words.clear()
        for i in req:
            words.append(i)
        tree.insert("", END, values=words)


def item_selected(event):
    global tree, edit, giv_date, ret_date
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        id = tree.set(tree.selection(), 0)
        name = tree.set(tree.selection(), 1)
        col = tree.set(tree.selection(), 2)
        mat = tree.set(tree.selection(), 3)
        pri = tree.set(tree.selection(), 4)
        boo = tree.set(tree.selection(), 5)
        date_giv = tree.set(tree.selection(), 6)
        date_ret = tree.set(tree.selection(), 7)
    edit = tk.Tk()
    edit.minsize(550, 650)
    edit.maxsize(550, 650)
    edit.title("Редактировать")
    color_values = get_colors()
    material_values = get_materials()
    book_values = get_book()
    tk.Label(edit, text="НАИМЕНОВАНИЕ").pack(anchor="center")
    naming = tk.Entry(edit)
    naming.insert(0, f"{name}")
    naming.pack(anchor="center", pady=10)
    tk.Label(edit, text="ЦВЕТ").pack(anchor="center")
    color = ttk.Combobox(edit)
    color['values'] = color_values
    color.set(f"{col}")
    color.pack(anchor="center", pady=10)
    tk.Label(edit, text="МАТЕРИАЛ").pack(anchor="center")
    material = ttk.Combobox(edit)
    material['values'] = material_values
    material.set(f"{mat}")
    material.pack(anchor="center", pady=10)
    tk.Label(edit, text="ЦЕНА").pack(anchor="center")
    price = ttk.Entry(edit)
    price.insert(0, f"{pri}")
    price.pack(anchor="center", pady=10)
    tk.Label(edit, text="БРОНЬ").pack(anchor="center")
    books = ttk.Combobox(edit)
    books['values'] = book_values
    books.set(f"{boo}")
    books.pack(anchor="center", pady=10)
    tk.Label(edit, text="ДАТА ВЫДАЧИ").pack(anchor="center")
    try:
            cur.execute(f"SELECT req_date_give, req_date_return from requisite WHERE req_id = {id}")
            dating = cur.fetchone()
            dgive = dating[0]
    except:
            dgive = "-"
    try:
            cur.execute(f"SELECT req_date_give, req_date_return from requisite WHERE req_id = {id}")
            dating = cur.fetchone()
            dret = dating[1]
    except:
            dret = "-"
    giv_date = tkcalendar.DateEntry(edit, width=12, background='darkblue', foreground='white',
                                        borderwidth=2)
    giv_date.pack(padx=10, pady=10)
    tk.Label(edit, text="ДАТА ВОЗВРАЩЕНИЯ").pack(anchor="center")
    ret_date = tkcalendar.DateEntry(edit, width=12, background='darkblue', foreground='white',
                                        borderwidth=2)
    ret_date.pack(padx=10, pady=10)
    submit_btn = tk.Button(edit, text="Сохранить",
                               command=lambda: apply(id, naming, color, material, price, books, giv_date, ret_date))
    submit_btn.pack(anchor="center", pady=10)
    tk.Label(edit, text="Внимательно смотрите на даты, они сбрасываются при открытии окна").pack(pady=10)
    tk.Label(edit, text=f"Старые даты: \n Выдача: {dgive}, возврат: {dret}").pack(pady=10)


def apply(id, naming, color, material, price, books, giv_date, ret_date):
    global edit
    name = naming.get()
    col = color.get()
    mat = material.get()
    pri = price.get()
    boo = books.get()
    giv = giv_date.get()
    ret = ret_date.get()

    cur.execute(f"SELECT col_id from colors WHERE col_name = '{col}'")
    col_id = cur.fetchone()[0]
    cur.execute(f"SELECT mat_id from materials WHERE mat_name = '{mat}'")
    mat_id = cur.fetchone()[0]
    cur.execute(f"SELECT book_id from booked WHERE book_name = '{boo}'")
    boo_id = cur.fetchone()[0]
    g = (f"{giv}".split('/'))
    if int(g[0]) < 10:
        g = '-'.join(f"{giv}".split('/'))
        g = '0' + f'{g}'
    else:
        g = '-'.join(f"{giv}".split('/'))
    gg = datetime.datetime.strptime(g, "%m-%d-%y")
    gg = gg.strftime("%Y-%m-%d")

    r = '-'.join(f"{ret}".split('/'))
    if int(r[0]) < 10:
        r = '-'.join(f"{ret}".split('/'))
        r = '0' + f'{r}'
    else:
        r = '-'.join(f"{ret}".split('/'))
    rr = datetime.datetime.strptime(r, "%m-%d-%y")
    rr = rr.strftime("%Y-%m-%d")
    cur2.execute(f"UPDATE requisite SET req_name = '{name}', req_col = {col_id}, req_mat = {mat_id}, req_price = {pri},"
                 f" req_booked = {boo_id}, req_date_give = '{gg}', req_date_return = '{rr}' WHERE req_id = {id}")
    con.commit()
    edit.destroy()


def authorize():
    global user_id, role
    logging = log.get()
    passwording = pwd.get()
    if (logging != '') and (passwording != ''):
        if logging == 'kassa1' and passwording == '777':
            user_id = logging
            admin()

        elif logging == 'kassa2' and passwording == '7777':
            user_id = logging
            admin()
        else:
            tk.messagebox.showwarning("Внимание", "Неправильно введён логин или пароль")
    else:
        tk.messagebox.showwarning("Внимание", "Введите логин и пароль")


# cur.execute("CREATE TABLE materials (mat_id INTEGER IDENTITY(1,1) PRIMARY KEY, mat_name VARCHAR(50))")
# cur.execute("CREATE TABLE booked (book_id INTEGER IDENTITY(1,1) PRIMARY KEY, book_name VARCHAR(50))")
# cur.execute("CREATE TABLE colors (col_id  INTEGER IDENTITY(1,1) PRIMARY KEY, col_name VARCHAR(50))")
# cur.execute("CREATE TABLE payment (pay_id  INTEGER IDENTITY(1,1) PRIMARY KEY, pay_name VARCHAR(11))")
# cur.execute("CREATE TABLE prof (pro_id  INTEGER IDENTITY(1,1) PRIMARY KEY, pro_name VARCHAR(30))")
# cur.execute("CREATE TABLE client (cl_id INTEGER IDENTITY(1,1) PRIMARY KEY, cl_name VARCHAR(65), cl_phone VARCHAR(12), cl_address VARCHAR(60), cl_birthday VARCHAR(15), cl_snils VARCHAR(11), cl_stud VARCHAR(10), cl_pro INTEGER REFERENCES prof(pro_id), cl_link VARCHAR(70))")
# cur.execute("CREATE TABLE requisite (req_id INTEGER IDENTITY(1,1) PRIMARY KEY, req_name VARCHAR(65), req_mat INTEGER REFERENCES materials(mat_id), req_col INTEGER REFERENCES colors(col_id), req_price INTEGER, req_booked INTEGER REFERENCES booked(book_id), req_date_give VARCHAR(20), req_date_return VARCHAR(20)")
# cur.execute("CREATE TABLE orders (ord_id INTEGER IDENTITY(1,1) PRIMARY KEY, ord_client INTEGER REFERENCES client(cl_id), ord_costumes VARCHAR(255), ord_booked INTEGER REFERENCES booked(book_id), ord_date_give VARCHAR(15), ord_date_return VARCHAR(15), ord_price INTEGER, ord_payment INTEGER REFERENCES payment(pay_id), ord_uncomplete VARCHAR(5))")
# cur.execute("CREATE TABLE order_content (oc_id INT IDENTITY PRIMARY KEY, oc_order INT FOREIGN KEY REFERENCES orders(ord_id), oc_content INT FOREIGN KEY REFERENCES requisite(req_id))")
global win
win = tk.Tk()
win.title("АВТОРИЗАЦИЯ")
win.geometry("600x400")
win.minsize(600, 400)
win.maxsize(1200, 800)
ttk.Label(win, text="Авторизация").pack(anchor="center")
ttk.Label(win, text="Логин").pack(anchor="center", pady=[50, 1])
log = ttk.Entry(win)
log.pack()
ttk.Label(win, text="Пароль").pack(anchor="center", pady=[25, 1])
pwd = ttk.Entry(win)
pwd.pack()
login = ttk.Button(text="Войти", command=authorize)
login.pack(anchor="center", pady="50")

win.mainloop()
a = input()
