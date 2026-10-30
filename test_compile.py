import py_compile

py_compile.compile('ir_db.py', doraise=True)
py_compile.compile('incident_workflow.py', doraise=True)
py_compile.compile('main_ir.py', doraise=True)
print('OK')
