for filename in Data/*.pdf; do
	pdftotext -enc ASCII7 "$filename"
done