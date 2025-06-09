**How to Setup Python Game Arcade:**

**1. MySQL Setup:** 

        -- Creating the database
        
        CREATE DATABASE IF NOT EXISTS game;
        
        -- Selecting the database
        
        USE game;
        
        -- Creating the create_account table
        
        CREATE TABLE IF NOT EXISTS create_account (
          userid INT PRIMARY KEY,
          email VARCHAR(255) NOT NULL,
          username VARCHAR(50) NOT NULL,
          mobile_no VARCHAR(15) NOT NULL,
          pass VARCHAR(255) NOT NULL,
          confirmpass VARCHAR(255) NOT NULL,
          descrip TEXT,
          score_mario VARCHAR(50),
          score_shooter VARCHAR(50),
          score_flappy VARCHAR(50),
          score_space VARCHAR(50),
          rating_mario VARCHAR(50),
          rating_shooter VARCHAR(50),
          rating_flappy VARCHAR(50),
          rating_space VARCHAR(50),
          profile_photo VARCHAR(255),
          Recently_played TINYINT,
          played_time INT
      );


**2. Install All Dependencies:**

      pip install -r requirements.txt

**3. Screenshots for Demo Purpose:**

1.

![Screenshot 2025-06-09 221934](https://github.com/user-attachments/assets/0b76e1a4-f1be-48ff-bf4e-d7fc79489efc)

2.

![Screenshot 2025-06-09 221950](https://github.com/user-attachments/assets/4443c15a-0ff2-4bfd-b016-13f3f187a211)

3.

![Screenshot 2025-06-09 222008](https://github.com/user-attachments/assets/d3f54a70-47bb-4ade-9560-a44b7f867a25)

4.

![Screenshot 2025-06-09 222031](https://github.com/user-attachments/assets/c38f6d46-a85a-46b6-a6ab-b60ab25a1788)

5.

![Screenshot 2025-06-09 222204](https://github.com/user-attachments/assets/df1ab783-27b6-40a2-b558-7b7cbdc22d32)

6.

![Screenshot 2025-06-09 222426](https://github.com/user-attachments/assets/d3837860-09fd-4316-8470-433eb819ad17)

7.

![Screenshot 2025-06-09 222450](https://github.com/user-attachments/assets/6086918e-6903-44c5-ac87-f4e4b03417b0)

8.

![Screenshot 2025-06-09 223146](https://github.com/user-attachments/assets/ab20384b-b993-4ba8-979f-aba79aa69773)

9.

![Screenshot 2025-06-09 223209](https://github.com/user-attachments/assets/346cdbd2-b1a1-40c8-9739-22eca33899bb)

10.

![Screenshot 2025-06-09 223220](https://github.com/user-attachments/assets/690e7344-ab58-456f-be79-4bd8f0b8b87c)

11.

![Screenshot 2025-06-09 223250](https://github.com/user-attachments/assets/98f37779-9e4f-4d2a-8b3e-c442e39a63f0)

12.

![Screenshot 2025-06-09 223312](https://github.com/user-attachments/assets/12777322-5696-4c1a-a32e-d858bea9dc0e)



