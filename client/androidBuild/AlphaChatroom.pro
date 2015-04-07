TEMPLATE = app

win32 {
    ASM = $$find(SOURCES, ^.*\.asm$)
    SOURCES -= $$ASM

    masm.input = ASM
    masm.output = ${QMAKE_FILE_BASE}.obj

    contains(QMAKE_TARGET.arch, x86_64) {
        CONFIG += win32_x64
        masm.name = MASM64 compiler
        masm.commands = ml64 /Fo ${QMAKE_FILE_OUT} /c ${QMAKE_FILE_IN}
    } else {
        CONFIG += win32_x86
        masm.name = MASM compiler
        masm.commands = ml /Fo ${QMAKE_FILE_OUT} /c ${QMAKE_FILE_IN}
    }

    QMAKE_EXTRA_COMPILERS += masm
}

#CONFIG += warn_off release
CONFIG += debug
CONFIG -= app_bundle
QT += quick quickwidgets

RESOURCES = \
    resources/pyqtdeploy.qrc

SOURCES = pyqtdeploy_main.cpp pyqtdeploy_start.cpp pdytools_module.cpp
DEFINES += PYQTDEPLOY_FROZEN_MAIN
DEFINES += PYQTDEPLOY_OPTIMIZED
HEADERS = pyqtdeploy_version.h frozen_bootstrap.h frozen_main.h

DEFINES += XML_STATIC
INCLUDEPATH += /src/Python-3.4.3-and/Modules/expat
INCLUDEPATH += /src/Python-3.4.3-and/Modules
INCLUDEPATH += /src/Python-3.4.3-and/Modules/_ctypes
INCLUDEPATH += /home/step5/python_android/include/python3.4
INCLUDEPATH += /src/Python-3.4.3-and/Modules/_multiprocessing
# INCLUDEPATH += /usr/include

LIBS += -L/usr/local/ssl/android-21/lib
LIBS += -L/home/step5/python_android/lib/python3.4/site-packages -lsip
LIBS += -L/home/step5/python_android/lib/python3.4/site-packages/PyQt5 -lQt -lQtGui -lQtCore -lQtQml -lQtNetwork -lQtQuick -lQtWidgets -lQtQuickWidgets
#LIBS += -lcrypto
#LIBS += -lssl
LIBS += /usr/local/ssl/android-21/lib/libssl.a /usr/local/ssl/android-21/lib/libcrypto.a

#LIBS += -L/usr/local/lib
#LIBS += -lreadline
LIBS += /home/step5/android-ndk-r10d/platforms/android-21/arch-arm/usr/lib/libreadline.a
LIBS += /home/step5/android-ndk-r10d/platforms/android-21/arch-arm/usr/lib/libncurses.a
#LIBS += -lffi
LIBS += /home/step5/android-ndk-r10d/platforms/android-21/arch-arm/usr/lib/libffi.a

SOURCES += /src/Python-3.4.3-and/Modules/binascii.c
SOURCES += /src/Python-3.4.3-and/Modules/expat/xmltok.c
SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/stgdict.c
SOURCES += /src/Python-3.4.3-and/Modules/_math.c
SOURCES += /src/Python-3.4.3-and/Modules/mathmodule.c
SOURCES += /src/Python-3.4.3-and/Modules/mmapmodule.c
SOURCES += /src/Python-3.4.3-and/Modules/_datetimemodule.c
SOURCES += /src/Python-3.4.3-and/Modules/_pickle.c
SOURCES += /src/Python-3.4.3-and/Modules/sha512module.c
SOURCES += /src/Python-3.4.3-and/Modules/expat/xmlrole.c
SOURCES += /src/Python-3.4.3-and/Modules/md5module.c
SOURCES += /src/Python-3.4.3-and/Modules/_bisectmodule.c
SOURCES += /src/Python-3.4.3-and/Modules/_randommodule.c
SOURCES += /src/Python-3.4.3-and/Modules/_multiprocessing/multiprocessing.c
SOURCES += /src/Python-3.4.3-and/Modules/selectmodule.c
SOURCES += /src/Python-3.4.3-and/Modules/sha1module.c
SOURCES += /src/Python-3.4.3-and/Modules/sha256module.c
SOURCES += /src/Python-3.4.3-and/Modules/timemodule.c
SOURCES += /src/Python-3.4.3-and/Modules/_heapqmodule.c
SOURCES += /src/Python-3.4.3-and/Modules/arraymodule.c
SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/cfield.c
SOURCES += /src/Python-3.4.3-and/Modules/_ssl.c
SOURCES += /src/Python-3.4.3-and/Modules/_multiprocessing/semaphore.c
SOURCES += /src/Python-3.4.3-and/Modules/expat/xmlparse.c
SOURCES += /src/Python-3.4.3-and/Modules/_json.c
SOURCES += /src/Python-3.4.3-and/Modules/pyexpat.c
SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/callbacks.c
SOURCES += /src/Python-3.4.3-and/Modules/socketmodule.c
SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/_ctypes.c
SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/callproc.c

!win32 {
    DEFINES += HAVE_EXPAT_CONFIG_H
    LIBS += -L/home/step5/python_android/lib -lpython3.4
    SOURCES += /src/Python-3.4.3-and/Modules/readline.c
    SOURCES += /src/Python-3.4.3-and/Modules/_posixsubprocess.c
    SOURCES += /src/Python-3.4.3-and/Modules/grpmodule.c
}

macx {
    DEFINES += MACOSX
    INCLUDEPATH += /src/Python-3.4.3-and/Modules/_ctypes/darwin
    INCLUDEPATH += /src/Python-3.4.3-and/Modules/_ctypes/libffi_osx/include
    SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/libffi_osx/ffi.c
    SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/libffi_osx/x86/x86-darwin.S
    SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/libffi_osx/x86/x86-ffi_darwin.c
    SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/libffi_osx/x86/x86-ffi64.c
    SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/libffi_osx/x86/darwin64.S
    SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/darwin/dlfcn_simple.c
    SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/malloc_closure.c
}

win32 {
    DEFINES += COMPILED_FROM_DSP
    INCLUDEPATH += /src/Python-3.4.3-and/Modules/_ctypes/libffi_msvc
    LIBS += -L/home/step5/python_android/lib -lpython34
    SOURCES += /src/Python-3.4.3-and/PC/msvcrtmodule.c
    SOURCES += /src/Python-3.4.3-and/Modules/_winapi.c
    SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/libffi_msvc/prep_cif.c
    SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/libffi_msvc/ffi.c
    SOURCES += /src/Python-3.4.3-and/Modules/_ctypes/malloc_closure.c
}

linux-* {
    LIBS += -lutil -ldl
}

win32 {
    LIBS += -ladvapi32 -lshell32 -luser32 -lws2_32 -lole32 -loleaut32
    DEFINES += MS_WINDOWS _WIN32_WINNT=Py_WINVER NTDDI_VERSION=Py_NTDDI WINVER=Py_WINVER

    # This is added from the qmake spec files but clashes with _pickle.c.
    DEFINES -= UNICODE
}

macx {
    LIBS += -framework SystemConfiguration -framework CoreFoundation
}

contains(ANDROID_TARGET_ARCH,armeabi-v7a) {
    ANDROID_EXTRA_LIBS = \
        $$PWD/../../../../../usr/local/ssl/android-21/lib/libcrypto.so
}
