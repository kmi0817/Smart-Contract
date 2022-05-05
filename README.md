# Smart Contract 👍

### 1. **Infomation 👀**

| Type       | Language |
| ---------- | -------- |
| **Server** | Flask    |
| **Client** | Bootstrap|

### 2. **Build Flask**

- If Windows, remove 3 after python & pip

```
python3 -m venv myvenv // In cwd, create a virtual environment for Flask
source myvenv/bin/activate // Enter the virtual environment
pip3 install flask
pip3 install --upgrade pip // if necessary
```

### 3. **Start Flask 😍**

- Make sure that you're in the virtual envrionment
- If Windows, replace 'export' with 'set'

```
export FLASK_APP=app
export FLASK_ENV=development
python3 run.py
```

### 4. **Directory Structure**

- working on...

> ##### README.md
>
> ##### .gitignore
>
> run.py
>
> ##### app (directory)
>
> > ###### models (directory)
> >
> > ###### static (directory)
> >
> > ###### templates (directory)
> >
> > **init**.py
> >
> > routes.py

<hr>

## On the website, you can...
### **Sort Repositories**
- Default: Created date in the descending order
- Option1: Stars in the descending order
- Option2: Names in the ascending order

### **Search Repositories**
- You can search repositories by repository name
