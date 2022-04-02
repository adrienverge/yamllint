# CA Certificate should be kept in this directory and ignored by git
#
# The script that follows is a WIP so it isn't doing anything yet
# but the intent is to read all the *.crt and *.pem files and 
# do something like the following from the dockerfile
#
#ARG CA_DIR=/usr/local/share/ca-certificates/
#COPY certs/. ${CA_DIR}
#ENV NODE_EXTRA_CA_CERTS=/usr/local/share/ca-certificates/${PEM_FILENAME}
#RUN update-ca-certificates

# or
#=========================================================
# container with root credential
# this should work behind Cisco AnyConnect VPN
# docker cache lines are not reduced - future optimization

# syntax=docker/dockerfile:1
#FROM node:12-alpine as base

# Company CA Certificate
#ARG ca_file_crt=my_company.crt
# location of shared CA Certificate
#ARG ca_share_dir=/usr/local/share/ca-certificates/
# concatinated bundle of all CA Certificate
#ARG ca_bundle_all=/etc/ssl/certs/ca-certificates.crt

# 2 location on container for project
#WORKDIR /app

# 3 copy from local to WORKDIR
#COPY ./ca/${ca_file_crt} .

# 4-6 CA files to be added to container
#RUN mkdir ${ca_share_dir}
#RUN cp ${ca_file_crt} ${ca_share_dir}${ca_file_crt}
#RUN rm ${ca_file_crt}

# 7 upgrade alpine
#RUN apk --update upgrade

# 8 add each new CA to bundle file
#RUN cat ${ca_share_dir}${ca_file_crt} >> ${ca_bundle_all}

# 9 install curl and ca-certificates
#RUN apk add --no-cache curl ca-certificates

#10 run(update) Alpine ca-certificates 
#RUN update-ca-certificates
#=========================================================

# For now, this shell script will display the list of file names
# having read, Write and Execute permission
echo "The name of all files having all permissions :"
  
# loop through all files in current directory
for file in *
do

# check if it is a file
if [ -f $file ]
then

# check if it has all permissions
if [ -r $file -a -w $file -a -x $file ]
then

# print the complete file name with -l option
ls -l $file

# closing second if statement
fi

# closing first if statement
fi

done