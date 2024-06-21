import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  # For TLS
EMAIL_ADDRESS = 'tradelitcare@gmail.com'
EMAIL_PASSWORD = 'lvce opiv rkms udih'

def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_address, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Streamlit app
st.title("Contact Us")

# Contact Us Form
st.header("Contact Us")
contact_name = st.text_input("Name", key="contact_name")
contact_email = st.text_input("Email", key="contact_email")
contact_message = st.text_area("Message", key="contact_message")

if st.button("Submit"):
    if contact_name and contact_email and contact_message:
        # Send validation email to user
        validation_subject = "Thank you for contacting us!"
        validation_body = f"Hello {contact_name},\n\nThank you for getting in touch with us. We have received your message and will get back to you soon.\n\nBest regards,\nTradelit"
        if send_email(contact_email, validation_subject, validation_body):
            st.success("Thank you for contacting us! A validation email has been sent to you.")
            
            # Send collected data to your email
            feedback_subject = "New Contact Us Submission"
            feedback_body = f"Name: {contact_name}\nEmail: {contact_email}\nMessage: {contact_message}"
            if send_email(EMAIL_ADDRESS, feedback_subject, feedback_body):
                st.success("Your message has been sent to us successfully.")
            else:
                st.error("Failed to send your message to us.")
        else:
            st.error("Failed to send validation email.")
    else:
        st.error("Please fill out all fields.")

# Feedback and Rate Your Experience Form
st.header("Feedback and Rate Your Experience")
feedback_email = st.text_input("Email (for feedback confirmation and rating)", key="feedback_email")
feedback_message = st.text_area("Please provide your feedback", key="feedback_message")
rating = st.radio(
    "How would you rate your experience?",
    options=[
        "😡 Very Poor", "😟 Poor", "😐 Average", "😊 Good", "😁 Excellent"
    ],
    key="rating"
)

if st.button("Submit Feedback and Rating"):
    if feedback_email and (feedback_message or rating):
        feedback_subject = "Thank you for your feedback!"
        
        feedback_body = f"Hello,\n\nThank you for your feedback."
        if feedback_message:
            feedback_body += f"\n\nWe have received the following feedback from you:\n{feedback_message}\n\nWe have noted your feedback and will work to improve."
        
        if rating:
            if rating == "😡 Very Poor":
                feedback_body += "\n\nWe are sorry to hear that you had a very poor experience. We will strive to do better."
            elif rating == "😟 Poor":
                feedback_body += "\n\nWe are sorry to hear that you had a poor experience. Your feedback helps us improve."
            elif rating == "😐 Average":
                feedback_body += "\n\nThank you for your feedback. We aim to provide a better experience next time."
            elif rating == "😊 Good":
                feedback_body += "\n\nWe are glad to hear that you had a good experience. We will keep up the good work!"
            elif rating == "😁 Excellent":
                feedback_body += "\n\nWe are thrilled to hear that you had an excellent experience! Thank you for your feedback."

        feedback_body += "\n\nBest regards,\nTradelit"

        if send_email(feedback_email, feedback_subject, feedback_body):
            st.success("Thank you for your feedback! A confirmation email has been sent to you.")
            
            # Send feedback and rating to your email
            feedback_subject = "New Feedback and Rating Submission"
            feedback_body = f"Email: {feedback_email}"
            if feedback_message:
                feedback_body += f"\nFeedback: {feedback_message}"
            if rating:
                feedback_body += f"\nRating: {rating}"
            if send_email(EMAIL_ADDRESS, feedback_subject, feedback_body):
                st.success("Your feedback and rating have been sent to us successfully.")
            else:
                st.error("Failed to send your feedback and rating to us.")
        else:
            st.error("Failed to send confirmation email.")
    else:
        st.error("Please provide either feedback or a rating.")
