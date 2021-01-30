# Beid
Python for read belgian ID Card.

#### Python (3.x) Requirements
  * smartcard
  
#### API
  * read(device, informations=True, address=True, photo=True)
    * informations :
      * nationality
      * card_number
      * suffix
      * birthdate
      * first_name
      * national_number
      * start_date
      * end_date
      * sex
      * place_of_delivery
      * last_name
      * birthplace
    * address :
      * address
      * locality
      * postal_code
    * photo (bytearray).

#### Examples
  * ex1.py (informations only).
  * ex2.py (address only).
  * ex3.py (photo only + generate file).
  * example-electron-vue.
    ![alt](https://github.com/cruizsan/beid/raw/main/image.png)
