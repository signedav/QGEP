from PyQt4.QtCore import QSettings, QVariant, QLocale, QTranslator, QCoreApplication
import os
import logging

def setupI18n( thePreferredLocale=None):
    """
    Setup internationalisation for the plugin.

    See if QGIS wants to override the system locale
    and then see if we can get a valid translation file
    for whatever locale is effectively being used.

    @param thePreferredLocal will override any other locale setting
    """
    
    logger = logging.getLogger( __name__ )
    
    myOverrideFlag = QSettings().value('locale/overrideFlag',
                                        QVariant(False)).toBool()
                                        

    myLocaleName = None
    if thePreferredLocale is not None:
        myLocaleName = thePreferredLocale
        logger.info( 'Using preferred locale: ' + myLocaleName )
    elif myOverrideFlag:
        myLocaleName = QSettings().value('locale/userLocale',
                                         QVariant('')).toString()
        logger.info( 'Using QGIS override locale: ' + myLocaleName )
    else:
        myLocaleName = QLocale.system().name()
        # NOTES: we split the locale name because we need the first two
        # character i.e. 'id', 'af, etc
        myLocaleName = str(myLocaleName)
        logger.info( 'Using system default locale: ' + myLocaleName )

    # Insert into QT's translation system
    # As soon as translator gets deleted, the translation will stop
    # Therefore, QCoreApplication is set as parent to not delete it
    # while the application is running (but we might end up loading
    # the same translation twice)
    translator = QTranslator( QCoreApplication.instance() )
    
    myTranslatorFile = 'qgepplugin_' + myLocaleName
    
    myResult = translator.load( myTranslatorFile, ':/plugins/qgepplugin/i18n' )
    
    if myResult:
        QCoreApplication.instance().installTranslator( translator )