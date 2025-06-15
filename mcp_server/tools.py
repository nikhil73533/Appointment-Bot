# Create a user identity,Take name, phone number and email.
# Create appointment Ask for three things Name, phone number, Appontment Type, Date and time, with whome. 
# Delete appointment
# List all the appointment for that user only.
# For editing appointment ask appoint number, or user email, Appointment Type or with whome.

import uuid
from mcp_server.utils import validate_email,validate_phone
from mcp_server.db_helper import DbHlper

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os

db = DbHlper()
# Automatic email 
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv('SENDER_PASSWORD')
smtp_server = 'smtp.gmail.com'
smtp_port = 587

def register_user(user_name:str,user_email:str,phone_number:str):
    """ Register user function registers or create a new of a user into database. 
        For that function following required parameters.  You must provide the arguments in provided sequence only.
    Args:
        user_name (str): Name of a user 
        user_email (str): email of a user eg. jhondoe@gmail.com
        phone_number (str): 10 digit phone number of user 

    Returns:
        str: Success or failour message.
    """
    try:
        # Initializing the user id
        user_id = str(uuid.uuid4())
        user_table = "Users"

        # validating the email addres. 
        if(validate_email(user_email)==False):
            return "Invalid user email"
        if(validate_phone(phone_number)==False):
                return "Invalid phone number"
        
        # Creating the user table. 
        user_schema = {
            "user_id": {"type": "TEXT", "nullable": "NOT NULL"},
            "user_name": {"type": "TEXT", "nullable": "NOT NULL"},
            "user_email": {"type": "TEXT", "nullable": "NOT NULL"},
            "phone_number": {"type": "TEXT", "nullable": None}
                    }
        print("Creating schema.")
        result = db.create_schema(user_table,user_schema,primary_key="user_email")
        print("Schema created...")
        # Inserting the user data into the table. 
        sql_query  = """INSERT INTO Users (user_id, user_name, user_email, phone_number)
                        VALUES (?, ?, ?, ?)
                        """
        
        # Checking if user already exists or not. 
        check_query = """SELECT count(1) FROM Users WHERE user_email = ?"""
        count = db.run_sql(check_query,params=(user_email,))[0][0]
        print("Count: ",count)
        if(int(count) >0):
             print(f"User exists or not : {count} ")
             return "User already exists, Please Call appointment for this user"

        params = (user_id,user_name,user_email,phone_number)
        result = db.run_sql(sql_query,params)
        print(f"Result:{result}")
        return f"Successfully Registered the user"
    except Exception as e:
        print(f"While registering the user {e}")
        return "Failed to register the user"

def create_appointment(user_email,app_type:str,datetime:str,app_desc:str = ""):
    """ create_appointment will create an appointment with required parameters. Before calling this tool please ask user to provide these informations.
        You are restricted to provide the Arguments in provided sqeuence. Also this tool can send the email alert when appoitnment has booked. You must mention this into your response. 
    Args:
        user_email (str): Email of user required to identify the user.
        app_type (str): appointment type there are four types of appointent 1. Meeting, 2. Consultency, 3. Advice, 4.Interview.
        datetime (str): User must provide the datetime for an appointment.
        app_desc (str,optional): Description of an appointment this optional if not given by the user write by your self in 20 words keep it very short.Default to ""
    Returns:
        str: success / failed message.
    """
    try:
        # Fetch the user details using user email.
        appointment_table = "Appointments"
        sql_query = """SELECT * FROM Users WHERE user_email = ?"""
        appointment_id = str(uuid.uuid4())
        print("sql query:",sql_query)
        user_details = db.run_sql(sql_query,params=(user_email,))[0]
        if(user_details==None):
             return "Sorry, didn't find the details of this user please first call the register_user tool to register the user details then call this."
        print(user_details)
        # create an appointment table.
        app_schema = {
            "appointment_id": {"type": "TEXT", "nullable": "NOT NULL"},
            "user_name": {"type": "TEXT", "nullable": "NOT NULL"},
            "user_email": {"type": "TEXT", "nullable": "NOT NULL"},
            "phone_number": {"type": "TEXT", "nullable": None},
            "app_desc":{"type": "TEXT", "nullable": None},
            "app_type":{"type": "TEXT", "nullable": None},
            "datetime":{"type": "TEXT", "nullable": None},
            "user_id":{"type": "TEXT", "nullable": "NOT NULL"}
                    }
        
        result = db.create_schema(appointment_table,app_schema,primary_key="appointment_id",foreign_keys=[("user_id","Users","user_id")])

        # Inserting the user data into the table. 
        sql_query  = f"""INSERT INTO {appointment_table} (appointment_id, user_name, user_email, phone_number, app_desc,app_type,datetime,user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?,?)
                        """
        params = (appointment_id,user_details[1],user_details[2],user_details[3],app_desc,app_type,datetime,user_details[0])
        result = db.run_sql(sql_query,params)

        # Getting newly created appointment details.
        sql_query = f"""SELECT * FROM {appointment_table} WHERE appointment_id = ?"""
        result = db.run_sql(sql_query,(appointment_id,))


        try:
            subject = f"New Appointment Created at {datetime}"
            body = (f"Hi {user_details[1]}:\n\n"
                        f"Hope you are well"
                            f"This is a confirmation email that your appointment {datetime} has confirmed."
                            f"Appointment Type: {app_type}\n\n"
                            f"Thanks & Regards\n\nAutomated Bot")

            # Sending the email.    
            send_email(smtp_server, smtp_port, sender_email, sender_password,
                                user_email, subject, body)
        except Exception as e:
            print(f"While sending the email.. {e}")
            pass



        print(f"Result:{result}")
        return f"New appointment has created\n{result}"
    except Exception as e:
         print(f"while creating appointment {e}")
         return "Failed to create an appointment"
    

def update_appointment(appointment_id:str,datetime:str|None,app_desc:str | None,app_type:str | None):
    """ The update_appointment tool will update the appointment's datetime or appointment type, or appointment_description. 
    Required parameters appointmnet_id and optional parameters are datetime, appointment description and appointment type. 
    If you found any parameter value not found then must provide None to that parameter. You must provide the parameters in below sequence.
    Also this tool can send the email alert when appoitnment has updated. You must mention this into your response. 
    Required Args:
        appointment_id (str): Appointment id which user will provide. 
        datetime(str): Datetime of the appintment date.default(None)
        app_desc(str): Description of appointment.default(None)
        app_type(str): appoinment type eg: Interview, Meeting, Consultancy etc.default(None)

    Returns:
        str: success message. 
    """
    try:
            # Get the apointment by appointment id.
        sql_query = """SELECT * FROM Appointments WHERE appointment_id = ?"""
        details = db.run_sql(sql_query,params=(appointment_id,))[0]
        try:
            subject = f"Updated the apointment with Appointment Id: {appointment_id}"
            body = (f"Hi there! :\n\n"
                        f"Hope you are well"
                            f"This is a confirmation email that your appointment has updated."
                            f"Thanks & Regards\n\nAutomated Bot")

            # Sending the email.    
            send_email(smtp_server, smtp_port, sender_email, sender_password,
                                details[2], subject, body)
        except Exception as e:
            print(f"While sending the email.. {e}")
            pass
        
        # Updating the details.
        if(datetime!=None):
            result = db.edit("Appointments","datetime",datetime,"appointment_id")
            return f"Successfully updated the appointment date and time\n{details}"
        if(app_desc!=None):
            result = db.edit("Appointments","app_desc",app_desc,"appointment_id")
            return f"Successfully updated the appointment appointment description\n{details}"
        if(app_type!=None):
            result = db.edit("Appointments","app_type",app_type,"appointment_id")
            return f"Successfully updated the appointment type\n{details}"
        else:
            return "Please provide any following details to udpate datetime or appointment descrition and appointment type"
        
    except Exception as e:
            print(f"Whie updating the appointment {e}")
            return "Failed to update the appointment"
    


def fetch_details(sql_query,param):
    """fetch_details tool will provide you the appointment details or user datails. You can fetch the releven data using this tool.
        But for that you need to provide the bellow required parameters in sequential manner.
    Args:
        sql_query (str): Sql query to fetch the details.
        param (str): data that will need to run that sql query or data using which we are facing the details.
    Returns:
      (tuple) : user details
    """
    try:
        sql_query = """SELECT * FROM Appointments WHERE user_email = ?"""
        # sql_query = sql_query.replace("sql_query=","").replace('""',"''")
        print((param,))
        results = db.run_sql(sql_query,params=(param.strip(),))[0]
        print(f"Results: {results}")
        return results
    except Exception as e:
         print(f"While running the sql query {e}")
         return "Failed to fetch the result."

def delete_appointment(appointment_id:str, user_email:str):
    """ This function deletes the appointment from the database.
        Please ask the required parameters you can ask either appointment id or email id. 
        if user provides email id then you must provide None for appointment id and visa versa. 
    Optional Args:
        appointment_id (str): Appointment id which user will provide. 
        user_email (str): User email. 
    Returns:
        str: success message. 
    """
    try:
        
        if(appointment_id== None):  
            # Get the apointment by appointment id.
            sql_query = """SELECT * FROM Appointments WHERE user_email = ?"""
            details = db.run_sql(sql_query,params=(user_email,))[0]
            print(f"Details: {details}")
            appointment_id =  details[0]

        result = db.delete("Appointments","appointment_id",appointment_id)
        return "Successfully deleted the appointment"
    except Exception as e:
        print(f"While deleting the appointment")
        return "Failed to delete the appointment"
    
    

def send_email(smtp_server, smtp_port, sender_email, sender_password,
               recipient_email, subject, body):
    """Compose and send an email with an optional PDF attachment."""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()





def greetings(query):
     """ This action will provide you greetings. To use this you must provide None requrired parameter. 
     query:
        query(str): Query will be user query eg. Hi, Hello, How are you? 
    Returns:
        str: Greetings to user.
    """
     return "How May I help you ?"






# def create_conversations(conversations:list[str]):
#     try:
#         # Cre
#     except Exception as e:
#         print(f"While Creating the conversations {e}")
#         return "Failed to create a conversations."
    
# def feteh_conversations():
#     try:
#     except Exception as e:
#         print(f"Whle fetchng the conversations {e}")

# if __name__ == "__main__":
#     user_name = "Jhone Doe"
#     user_email = "jhonedoe@gmail.com"
#     phone_number = "9352400502"
#     app_type = "Interview"
#     datetime=  "22/04/2025:1:10PM"
#     appoint_id = "e3c6c441-61ca-4ecc-9e20-ed1f2c778bed"
#     inp = (user_name,user_email,phone_number)
#     # result = register_user(*inp)
#     # result = create_appointment(user_email,app_type,datetime)
#     # result = update_appointment(appoint_id,app_desc="This is test update..")
#     result = delete_appointment(appoint_id)
#     # print(f"Function doc string. {register_user.__doc__}")
#     print(f"result: {result}")