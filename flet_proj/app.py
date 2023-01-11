#modules
import flet
from flet import *
from datetime import datetime
import sys
import pathlib
import sqlite3


class Database:
    def ConnectToDatabase():
        try:
            db = sqlite3.connect('New.db')
           
            cur = db.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS tasks (ID INTEGER PRIMARY KEY, Task VARCHAR(255) NOT NULL, Date VARCHAR(255) NOT NULL)')
            return db
        except Exception as e:
            print(e)
            
    def ReadDatabase(db):
        cur = db.cursor()
        cur.execute('SELECT Task, Date FROM tasks')
        records = cur.fetchall()
        return records
    
    def InsertDatabase(db,values):
        cur = db.cursor()
        cur.execute('INSERT INTO tasks(Task, Date) VALUES(?, ?)', values)
        db.commit()
        return db
        
        
    def DeleteDatabase(db, value):
        cur = db.cursor()
        cur.execute('DELETE FROM tasks WHERE Task=?', value)
        db.commit()
        
    def UpdateDatabase(db, value):
        cur = db.cursor()
        cur.execute("UPDATE tasks SET Task=(?) WHERE Task=(?)", value)
        db.commit()
        




class FormContainer(UserControl):
    def __init__(self, func):
        self.func = func
        super().__init__()
        
        
    def build(self):
        return Container(
            width=280,
            height=80,
            bgcolor='#0c5703',
            opacity=0,
            border_radius=40,
            margin=margin.only(left=-20, right=-20),
            animate=animation.Animation(400, 'decelerate'),
            animate_opacity=200,
            padding=padding.only(top=45, bottom=45),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    TextField(
                        height=48, 
                        width=255,
                        filled=True,
                        border_color='transparent',
                        text_size=12,
                        color='black',
                        hint_text='My note is... ',
                        hint_style=TextStyle(size=11, color='black')
                        
                    ),
                    
                    IconButton(content=Text('Add Note'),
                               width=180,
                               height=44,
                               on_click=self.func,
                               style=ButtonStyle(
                               bgcolor={'': 'green'},
                               shape={
                                    '': RoundedRectangleBorder(radius=8)}
                               
                               ),
                        
                    )
                ]
                
            )
            
            
            
            
        )
    


#write code here
class CreateTask(UserControl):
    def __init__(self, task:str, date:str, func1, func2):
        self.task = task
        self.date = date
        self.func1 = func1
        self.func2 = func2
        super().__init__()
        
    def TaskDeleteEdit(self, name, color, func):
        return IconButton(
            icon=name, 
            width=30,
            icon_size=18,
            icon_color=color,
            opacity=0,
            animate_opacity=200,
            # change later....
            on_click=lambda e: func(self.GetContainerInstance())
            
        )
    def GetContainerInstance(self):
        return self
    
    
    
    
    def ShowIcons(self, e):
        if e.data == 'true':
            (e.control.content.controls[1].controls[0].opacity,
            e.control.content.controls[1].controls[1].opacity) = (
                1, 1
                
            )
            e.control.content.update()
        else:
            (e.control.content.controls[1].controls[0].opacity,
            e.control.content.controls[1].controls[1].opacity) = (
                0, 0

            )
            e.control.content.update()
            
    def build(self):
        return Container(
            width=280, 
            height=60, 
            border=border.all(0.85, 'white54'),
            border_radius=8,
            on_hover=lambda e: self.ShowIcons(e),
            clip_behavior=ClipBehavior.HARD_EDGE,
            padding=10,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        spacing=1,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text(value=self.task, size=10),
                            Text(value=self.date, size=9, color='white54'),
                            
                        ]
                        
                        
                    ),
                    Row(
                        spacing=0,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.TaskDeleteEdit(icons.DELETE_ROUNDED, 'red500', self.func1),
                            self.TaskDeleteEdit(icons.EDIT_ROUNDED, 'white70', self.func2),
                            
                            
                        ]
                        
                    )
                    
                ]
                
            )
            
        )


def main(page: Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    
    def AddTaskToScreen(e):
        
       
        
        dateTime = datetime.now().strftime('%b %d, %Y %I:%M')
        
       
        db = Database.ConnectToDatabase()
        Database.InsertDatabase(db, (form.content.controls[0].value, dateTime))
        
        db.close()
        
        
        if form.content.controls[0].value:
            _main_column_.controls.append(
                
                CreateTask(
                    form.content.controls[0].value,
                    dateTime,
                    DeleteFunction,
                    UpdateFunction,
                )
            )
            _main_column_.update()
            
            
            CreateToDoTask(e)
        else:
            db.close()
            pass
        
    def DeleteFunction(e):
        db = Database.ConnectToDatabase()
        Database.DeleteDatabase(db, (e.controls[0].content.controls[0].controls[0].value,)
        )
        db.close()
        
        _main_column_.controls.remove(e)
        _main_column_.update()
        
    
    def UpdateFunction(e):
        
        form.height, form.opacity = 200, 1
        (
            form.content.controls[0].value,
            form.content.controls[1].content.value,
            form.content.controls[1].on_click,
        ) = (e.controls[0].content.controls[0].controls[0].value,
            'Update',
            lambda _: FinalizeUpdate(e),
        )
        form.update()
    
    def FinalizeUpdate(e):
        db = Database.ConnectToDatabase()
        Database.UpdateDatabase(
            db,
            (
                form.content.controls[0].value,
                
                e.controls[0].content.controls[0].controls[0].value
            )
            
        )
        
        e.controls[0].content.controls[0].controls[0].value = form.content.controls[0].value
        e.controls[0].content.update()    
        
       
        
        CreateToDoTask(e)
        
        
    def CreateToDoTask(e):
        if form.height != 200:
            form.height, form.opacity = 200, 1
            form.update()
        else:
            form.height, form.opacity = 80, 0
            
            form.content.controls[0].value = ''
            form.content.controls[1].content.value = 'ADD NOTE'
            form.content.controls[1].on_click = lambda e: AddTaskToScreen(e)
            
            
            form.update()
            
               
    
    
    _main_column_ = Column(
        scroll='hidden',
        expand=True,
        alignment=MainAxisAlignment.START,
        controls=[
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text('Notes',size=18,weight='bold'),
                    IconButton(
                        icons.ADD_CIRCLE_ROUNDED,
                        icon_size=18,
                        on_click=lambda e: CreateToDoTask(e),
                        
                    ),
                    
                    
                ],
            ),
            Divider(height=8, color='white24')
        ],
    )
    page.add(Container(
        width=1500, 
        height=800, 
        margin=-10, 
        bgcolor='blue',
        alignment=alignment.center,
        content=Row(
            alignment=MainAxisAlignment.CENTER, 
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                
                Container(
                    width=280, 
                    height=600, 
                    bgcolor='#3e9934',
                    border_radius=40,
                    border=border.all(0.5, 'black'),
                    padding=padding.only(top=35, left=20, right=20),
                    clip_behavior=ClipBehavior.HARD_EDGE,
                    content=Column(
                        alignment=MainAxisAlignment.CENTER,
                        expand=True,
                        controls=[
                            _main_column_,
                            FormContainer(lambda e: AddTaskToScreen(e)),
                            
                            
                        ]
                        
                    )
                    
                    
                )
            ]
            
            
            
        )
        
        
    ))
    page.update()
    
    
    form = page.controls[0].content.controls[0].content.controls[1].controls[0]
    
    
    db = Database.ConnectToDatabase()

    for task in Database.ReadDatabase(db)[::-1]:
    
        _main_column_.controls.append(
        
            CreateTask(
            task[0],
            task[1],
            DeleteFunction,
            UpdateFunction,
            
            
        )

) 
    _main_column_.update()
    

if __name__ == '__main__':
    flet.app(target=main)



