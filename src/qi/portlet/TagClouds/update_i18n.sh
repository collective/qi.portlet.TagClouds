#!/bin/bash 
# start with ./update_i18n.sh
 
PRODUCT="qi.portlet.TagClouds"

# if you want to add new language, add the language
# to the following list (separated by space)
LANGUAGES='en cs fr de es eu'
for lang in $LANGUAGES; do
    mkdir -p locales/$lang/LC_MESSAGES/
    touch locales/$lang/LC_MESSAGES/$PRODUCT.po
done

i18ndude rebuild-pot --pot locales/$PRODUCT.pot --create $PRODUCT ./

# filter out invalid PO file headers. i18ndude sync adds them to the file, 
# but i18ntestcase fails if these headers are there
for lang in $LANGUAGES; do
    i18ndude sync --pot locales/$PRODUCT.pot locales/$lang/LC_MESSAGES/$PRODUCT.po
    mv locales/$lang/LC_MESSAGES/$PRODUCT.po locales/$lang/LC_MESSAGES/$PRODUCT.potmp
    grep -vE "^\"(Language|Domain).*" locales/$lang/LC_MESSAGES/$PRODUCT.potmp  >locales/$lang/LC_MESSAGES/$PRODUCT.po
    rm  locales/$lang/LC_MESSAGES/$PRODUCT.potmp
done
