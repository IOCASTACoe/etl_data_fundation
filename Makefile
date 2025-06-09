apaga_cache:
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
teste:
	ls -al

teste_post:
	cd /home/vscode/data/new/file/BIO/especies_ameacadas/20240101/00
curl -X 'POST' \
'http://127.0.0.1:8000/uploadfiles/' \
-H 'accept: application/json' \
-H 'Content-Type: multipart/form-data'   \
-F 'files=@dd_bio_sp_end_20240101.xlsx' \
-F 'files=@pnt_bio_sp_end_20240101.gpkg'\
-F 'files=@sld_bio_sp_end_20240101.sld' \
-F 'files=@md_bio_sp_end_20240101.xml'