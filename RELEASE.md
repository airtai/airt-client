# Release Notes

## 2022.11.0

Released on Nov 29, 2022

**airt-server changes:**

* Fix: Internal bugs

**airt-client changes:**

* Fix: Update prediction examples

## 2022.10.0

Released on Oct 29, 2022

**airt-server changes:**

* Feature: Accept both TOTP and SMS OTP for validation in token route
* Fix: Update error messages to use uuid instead of id
* Fix: Broken links generated by prediction to_local route

**airt-client changes:**

* Feature: Integrate token route changes
* Fix: Include working examples in the docstrings of all methods

## 2022.9.0

Released on Sep 30, 2022

**airt-server changes:**

* Feature: Rename from_csv, from_parquet routes to to_datasource route
* Feature: Add new routes to register and validate the phone number
* Feature: Add new route to reset password
* Feature: Add new route to send OTP via SMS to the registered phone number
* Feature: Accept both TOTP and SMS OTP for validation in disable_mfa and reset_password routes
* Feature: Add cloud_provider parameter in datablob routes to store datablob in aws or azure
* Fix: Add phone number field in /user/create route
* Fix: Remove password field in /user/update route
* Fix: Remove OTP requirement for read-only /user and /apikey routes

**airt-client changes:**

* Feature: Integrate to_datasource method and remove from_csv, from_parquet methods
* Feature: Integrate register and validate the phone number routes
* Feature: Integrate reset password route
* Feature: Integrate send SMS OTP route
* Feature: Integrate disable_mfa route changes
* Feature: Integrate cloud_provider changes
* Fix: Integrate user and apikey route changes

## 2022.8.0

Released on Aug 31, 2022

**airt-server changes:**

* Feature: Add GitHub as an external authentication provider for single sign-on (SSO)
* Feature: Use UUID instead of incremental id
* Feature: Add route to create datablob from Azure Blob Storage
* Feature: Add route to push prediction results to Azure Blob Storage

**airt-client changes:**

* Feature: Integrate single sign-on (SSO) changes
* Feature: Integrate UUID changes
* Feature: Integrate from_azure_blob_storage and to_azure_blob_storage routes
* Fix: Use .uuid attribute instead of the .id attribute to access the unique id for the class instances

## 2022.7.0

Released on Aug 1, 2022

**airt-server changes:**

* Fix: Get currently logged-in user information by passing either user_id or username
* Feature: Request OTP while accessing sensitive routes for MFA-enabled users
* Feature: Add parameter for specifying AWS region while creating new datablob to store data
* Feature: Add single sign-on (SSO) authentication for generating new tokens using Google as an external authentication provider

**airt-client changes:**

* Fix: Integrate user's info route changes
* Feature: Integrate OTP route changes
* Feature: Make sensitive CLI commands interactive if OTP is not passed as an argument for MFA enabled user
* Feature: Integrate region parameter
* Feature: Integrate single sign-on(SSO) authentication

## 2022.6.0

Released on June 1, 2022

**airt-server changes:**

* Feature: Add Multi-Factor authentication for login
* Feature: Add route to get user's info

**airt-client changes:**

* Feature: Integrate Multi-Factor authentication
* Feature: Integrate route to get user's info
* Fix: Include index_column in the output of the `airt model evaluate` CLI command

## 2022.5.0

Released on May 31, 2022

**airt-server changes:**

* Fix: Update OpenAPI docs
* Fix: Send the dtypes along with the data when calling the head route

**airt-client changes:**

* Fix: Add source for DataBlobs created using the from_local method
* Fix: Return a dictionary instead of pandas series when calling the Client.version method
* Fix: Set proper dtypes to the dataframe in the datasource.head method

## 2022.4.0

Released on April 27, 2022

**airt-server changes:**

* Fix: Include index of datasource in datasource head route's response
* Feature: Include datablob's source in datablob reponse object

**airt-client changes:**

* Feature: Integrate prediction.to_clickhouse method
* Feature: Add set_token method to Client class
* Fix: Include index of datasource in datasource.head() method
* Feature: Integrate source property in DataBlob class

## 2022.3.1

Released on April 13, 2022

**airt-server changes:**

* Fix: Update from_csv, from_parquet and from_clickhouse route parameter types

**airt-client changes:**

* Fix: Integrate from_csv, from_parquet and from_clickhouse route parameter changes

## 2022.3.0

Released on April 6, 2022

**airt-server changes:**

* Feature: Introduce DataBlob to import files from multiple sources
* Feature: Add from_local, from_s3, from_mysql, from_clickhouse routes to create DataBlob
* Feature: Add from_csv, from_parquet routes to create DataSource from DataBlob
* Feature: Add to_local, to_s3, to_mysql routes to push prediction results

**airt-client changes:**

* Feature: Introduce DataBlob Class to import files from multiple sources.
* Feature: Add from_local, from_s3, from_mysql and from_clickhouse methods to the DataBlob class for creating a new DataBlob.
* Feature: Add from_csv and from_parquet methods to create DataSource from a DataBlob.
* Feature: Update the ls method in all the classes to return the instances instead of a DataFrame.
* Feature: Add new method as_df to all the classes for returning the details in a DataFrame.
* Feature: Add to_local, to_s3, and to_mysql methods to push prediction results.
* Fix: Convert details, delete, and tag methods as instance methods.

## 2022.2.0

Released on February 28, 2022

**airt-server changes:**

* Fix: Update internal requirements' versions and dependencies' versions

**airt-client changes:**

* Fix: Update dependecies' versions

## 2022.1.0

Released on February 8, 2022

**airt-server changes:**

* Feature: Ability to create DataSource from multiple user uploaded CSV files
* Fix: Better error message if no csv file found in user uploaded files list

**airt-client changes:**

* Feature: Create DataSource using multiple user uploaded CSV files
* Fix: airt-client version error in README file

## 2021.12.0

Released on December 28, 2021

**airt-server changes:**

* Feature: New routes to create DataSource from user uploaded CSV

**airt-client changes:**

* Feature: Integrate routes for new user uploaded csv DataSource

## 2021.11.0

Released on November 30, 2021

**airt-server changes:**

* Feature: Implement new DataSource with Tag(s)
* Feature: Add route to get prediction push progress
* Feature: New route to update user info

**airt-client changes:**

* Fix: Rename authenticate function to get_token in API and CLI.
* Fix: Update error messages in CLI to display more meaningful information to the user.
* Feature: Integrate route for new DataSource with Tag(s)
* Feature: Integrate user create and list routes in CLI and API
* Feature: Add "disabled" and "completed" params to Datasource ls API
* Feature: Integrate Version, APIKey routes in CLI and API
* Feature: Integrate route to update user info
* Feature: Add link to REST API docs in client docs

## 2021.10.1

Released on October 25, 2021

**airt-server changes:**

* Feature: Add routes to create, revoke apikeys
* Fix: Update list objects routes
* Feature: Add pull for db datasource
* Fix: Add exception responses in openapi docs
* Fix: Remove connection params from response of datasource routes
* Fix: Created column value bug

**airt-client changes:**

* Feature: Add CLI interface
* Feature: Integrate list, delete, get details API for datasource, model and prediction objects
* Feature: Humanize date, filesize and time in CLI
* Feature: Add separate docs for CLI