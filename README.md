# To-Do List

### Description:
This is a to-do list webapp with a minimalistic aesthetic, made using the Flask framework.

The directory stucture of this project follows the basic Flask structure:
- `app.py` includes the python code for implementing Flask. 
- `templates/` contains the html files for each of the links within the webapp, with `layout.html` providing the base for other html files.
- `todolist.db` contains 2 tables: `users` stores the usernames and passwords; `tasks` stores the tasks created by each user.
- `static/styles.css` contains the stylings for the html files

When a user first opens the webapp, they are prompted to login or register for an account, after which they can access the main page of the web app.
Users can create a new task by typing on the text box and pressing 'Add'. The page will then reload and the new task added will be shown on the screen. 
I have debated on whether or not to make it so that a task can be added without the page reloading, however after extensive searching on the web I have failed to find a direct way to do it, if anyone has any advice I would love to hear it.

Users can check off a task by clicking on the checkbox and they can also delete a task by clicking on the 'x' button beside the task.
Users can also delete all completed tasks by click on 'Delete All Completed'.

Further improvements to this web app that I would like to do in the future include:
1. Archiving completed tasks so that users can still keep a backlog of the tasks they have done while keeping their main page clean.
2. Renaming tasks
3. Adding due date/time for a task
