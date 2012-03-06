@echo off
rem =========================
rem bricksviewer start script
rem =========================

set BV_CLASSPATH=lib/bricksviewer.jar
set BV_CLASSPATH=%BV_CLASSPATH%;lib/jdom.jar"
set BV_CLASSPATH=%BV_CLASSPATH%;lib/jogl.jar"

set NATIVE_CLASSPATH=lib/native

java "-Djava.library.path=%NATIVE_CLASSPATH%" -classpath "%BV_CLASSPATH%" net.sourceforge.bricksviewer.application.BricksViewerApplication
