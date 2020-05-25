# Fashion search engine

Posts and images retrieval engine for e-commerce data on multiple platforms on fashion domain. Images are restricted as single type product or only a model wearing a product in an image. Data in this project is crawled from 3 e-commerce platforms: [Tiki.vn](tiki.vn), [Shopee.vn](shopee.vn), and [Sendo.vn](sendo.vn)

# Setup environment and data

- Python 3 and ReactJS preinstalled
- Move to backend directory then run `pip install -r requirements.txt` to setup python environment for backend search engine
- From outer directory, move to fashion directory then run `npm install` to install packages for frontend search engine.
- Install Solr on your machine then create 2 new cores named multimedia (for posts data) and multimedia_shops (for shops data). Default port for solr service is **localhost:8983**
- From outer directory, run `./solr_script.sh` to create schema for our new cores. If you configure another port for Solr service, be sure to change port number in solr_script.sh.
- All required files include model for our search engine are available on: [This sharepoint](https://husteduvn-my.sharepoint.com/personal/thanh_lt163705_sis_hust_edu_vn/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fthanh%5Flt163705%5Fsis%5Fhust%5Fedu%5Fvn%2FDocuments%2Fdata%2Fmulti%5Fmedia%2Ffeature%5Ffrom%5Fpretrained&originalPath=aHR0cHM6Ly9odXN0ZWR1dm4tbXkuc2hhcmVwb2ludC5jb20vOmY6L2cvcGVyc29uYWwvdGhhbmhfbHQxNjM3MDVfc2lzX2h1c3RfZWR1X3ZuL0VuQWhJeTIwT3BOQ3VXWlNxVVRmSGZ3QlRtVzBRQ2ppLUVnUVpaVW1RcUQxVXc_cnRpbWU9Nk1Zc3duSUEyRWc). Download these following 4 files: all_feat.list, all_images_path.csv, features_resnet50.npy, res50_sz150_best_stage3_export.pkl to your download folder
- Move to `backend/` folder then change all paths in `settings.py` file corresponding to paths to your downloaded files above.
- Download images data for this search engine on [This sharepoint](https://husteduvn-my.sharepoint.com/:u:/g/personal/thanh_lt163705_sis_hust_edu_vn/EchO3VtpXRFKmGq1z9UFPkIBN_AkZ9tjlkOThdNbUxF4RQ?e=W73ZdN). Then create relative path from this images folder to public folder in `fashion` directory by running the following command: `ln -s path_to_your_images_folder this_project_folder/fashion/public`
- Download posts and shops data from [This sharepoint](). Create `data` directory on outer directory then move these downloaded data to this folder
- Push data to Solr cores: from outer directory, run `python -m backend.import_data`
- Now we are good to go

# Start program

- From outer directory, run `python -m backend.run_api` to start backend search APIs. Default port for backend services is **localhost:5000**
- Move to `fashion` folder, run `npm start` to start frontend service.

# Using program

We provide 2 services for users: 
- Firstly, you could choose text search type, type in your keywords you want to search and number of results
- Secondly, you could choose an image (single type product or only a model wearing the product you want to search) and number of results
Our program will return results corresponding to your input data and provide details of each product with a link to original post from the original platform having that post.
