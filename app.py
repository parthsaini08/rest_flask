from flask import Flask
from flask_restful import Resource,Api,reqparse,fields,abort,marshal_with
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///sqlite.db'
db=SQLAlchemy(app)


class Todomodel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(200))
    summary=db.Column(db.String(500))

#db.create_all()

resource_fields={
    'id':fields.Integer,
    'task':fields.String,
    'summary':fields.String,
}


#todos = {
#     1:{"task":"Write hello world program","summary":"Write code using python."},
#     2:{"task":"Task 2","summary":"Writing task 2"},
#     3:{"task":"Task 3","summary":"Writing task 3"}
# }
# class HelloWorld(Resource):
#     def get(self):
#         return {'data':'Hello ,world!'}

# class Helloname(Resource):
#     def get(self,name):
#         return {'data':'Hello , {}'.format(name)}

# api.add_resource(HelloWorld,'/helloworld')
# api.add_resource(Helloname,'/helloworld/<string:name>')

# get localhost:5000/helloworld
#hello world
# get localhost:5000/helloworld/parth
#hello parth

task_post_args=reqparse.RequestParser()
task_post_args.add_argument("task",type=str,required=True,help="Task is required")
task_post_args.add_argument("summary",type=str,help="summary is required",required=True)


task_put_args=reqparse.RequestParser()
task_put_args.add_argument("task",type=str)
task_put_args.add_argument("summary",type=str)

class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self,todo_id):
        task=Todomodel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404,message="Could not find task with the id")
        return task

    @marshal_with(resource_fields)
    def post(self,todo_id):
            args=task_post_args.parse_args()
            task=Todomodel.query.filter_by(id=todo_id).first()
            if task:
                abort(404,message="Could not find task with the id")
            todo=Todomodel(id=todo_id,task=args['task'],summary=args['summary'])
            db.session.add(todo)
            db.session.commit()
            return todo,201

    def delete(self,todo_id):
        task=Todomodel.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        return task

    @marshal_with(resource_fields)
    def put(self,todo_id):
        args=task_put_args.parse_args()
        task=Todomodel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404,message="Could not find task with the id")
        if args['task']:
            task.task=args['task']
        if args['summary']:
            task.summary=args['summary']
        db.session.commit()
        return task

class TodoList(Resource):
    def get(self):
        tasks=Todomodel.query.all()
        tods={}
        for task in tasks:
            tods[task.id]={"task":task.task,"summary":task.summary}
        return tods


api.add_resource(Todo,'/todos/<int:todo_id>')
api.add_resource(TodoList,'/todos')
if __name__=='__main__':
    app.run(debug=True)