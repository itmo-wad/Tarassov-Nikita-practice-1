# Tarassov-Nikita-practice-1
practice 1 25.03.2022
Required
1. Create a flask app which connects to MongoDB and runs at ‘http://localhost:5000’
2. Authentication

    User can sign up at ‘/signup’
    Login page at ‘/auth’ .If success, return a secret page to user. If not, give user a flash message about the error.
    Store username, password in database

3. Implement image upload feature

    Form to upload image at ‘/upload’
    Save uploaded image to folder ‘upload’ on server side, allow only specified extensions
    Redirect to ‘/uploaded/<filename>’ which shows the uploaded image
    Return user back to ‘upload’ with flash error message if there would be any error

Optional
4. Implement notebook at ‘/notebook’

    Page have a form for submitting new note (text only)
    Store submitted notes in database
    Display all saved notes below the form
    User can delete all notes
    User can limit the number of notes to be displayed in page

5. Implement chat bot at ‘/chatbot’

    Chat with bot without refreshing page
    Bot answer by simple rules
    Save chat history in database so refreshing page won’t delete it
    Allow user to clear chat history


At the end of the practice, you need to submit here link to a non-empty github repository (inside itmo-wad organization) with your code from this practice.
