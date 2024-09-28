### **Project Overview**

You have to build a crypto-based website that allows users to deposit funds and earn boosted liquidity for an upcoming project. The key functionalities include:

- Users can deposit between $1 and $10,000.
- Users select a lock period (in weeks) that determines how long their funds will be locked after the project launch.
- Users can deposit any cryptocurrency within the top 100 on the ETH mainnet.
- Deposited assets are swapped to USDC via Uniswap and transferred to a Gnosis Safe.
- The memo of the transaction includes the lock duration; defaults to 3 months if invalid.
- Backend processes transactions, validates memos, and stores data in a database.
- Frontend displays user-specific data (funds deposited, lock duration, etc.).
- Deployment of the website with domain linkage and database setup on Google Cloud.
- Integration of marketing efforts, including a Twitter presence.

---

### **Development and Integration**

#### **1. Frontend Development**

**1.1. Setup and Initial Configuration**

- **Task**: Set up the project using the existing React sample.
- **Tools**: React.js, Node.js, npm/yarn.
- **Action Items**:
  - Initialize the React project.
  - Install necessary dependencies (`ethers.js`, `Uniswap SDK`, wallet providers).

**1.2. User Interface Design**

- **Task**: Design the UI components for user interactions.
- **Action Items**:
  - Create input fields for deposit amount ($1 - $10,000).
  - Implement a dropdown menu for selecting cryptocurrencies (top 100 on ETH mainnet).
  - Add input for selecting lock duration in weeks.
  - Validate inputs (amount limits, valid weeks).

**1.3. Wallet Integration**

- **Task**: Integrate Bybit Wallet (or alternatives like MetaMask, WalletConnect).
- **Tools**: Bybit Wallet SDK, ethers.js.
- **Action Items**:
  - Implement wallet connection functionality.
  - Test wallet connections and ensure smooth user experience.

**1.4. Building Swap Transactions**

- **Task**: Integrate Uniswap to allow swapping deposited assets to USDC.
- **Tools**: Uniswap SDK, ethers.js.
- **Action Items**:
  - Fetch the list of supported tokens and liquidity pools from Uniswap.
  - Build functions to create swap transactions for selected tokens.
  - Ensure the swap and transfer to Gnosis Safe occur in a single transaction.
  - Display gas fee estimates and warnings about higher gas costs.

**1.5. Transaction Memo Inclusion**

- **Task**: Include lock duration in the transaction memo.
- **Action Items**:
  - Append the number of lock weeks to the transaction data.
  - Implement a default value of 3 months if the memo is invalid.

#### **2. Backend Development**

**2.1. Setting Up the Backend Server**

- **Task**: Create a backend server using Python Flask.
- **Tools**: Python 3.x, Flask, SQLite.
- **Action Items**:
  - Initialize the Flask application.
  - Set up necessary routes for API endpoints.

**2.2. Database Configuration**

- **Task**: Set up an SQLite database to store transaction data.
- **Action Items**:
  - Define the database schema:
    - User Address
    - Original Asset and Amount
    - USDC Amount Received
    - Lock Duration (Weeks)
    - Transaction Hash
    - Timestamp
  - Implement database connection and CRUD operations.

**2.3. Transaction Monitoring Script**

- **Task**: Develop a Python script to monitor transactions to the Gnosis Safe.
- **Tools**: Etherscan API, Web3.py or ethers.js (Python version).
- **Action Items**:
  - Use Etherscan API to fetch transactions to the Gnosis Safe address.
  - Parse transactions every new block or at set intervals.
  - Validate the memo field (lock duration); apply default if invalid.
  - Store transaction details in the SQLite database.
  - Handle rate limiting by optimizing API calls.

**2.4. Uniswap Pool Monitoring (Optional)**

- **Task**: Monitor and update the list of whitelisted liquidity pools.
- **Action Items**:
  - Set up a script to query Uniswap's subgraph for pool liquidity.
  - Update the list of supported tokens based on liquidity thresholds.

#### **3. Blockchain Interaction**

**3.1. Gnosis Safe Setup**

- **Task**: Create the Gnosis Safe multi-signature wallet to receive funds.
- **Tools**: Gnosis Safe interface or SDK.
- **Action Items**:
  - Collect wallet addresses of the signatories.
  - Set up the Gnosis Safe with the required signing policies.
  - Record the Gnosis Safe address for frontend and backend use.

**3.2. ETH Mainnet/Testnet Connection**

- **Task**: Connect the application to the ETH mainnet and a testnet for testing.
- **Tools**: Infura or Alchemy API keys.
- **Action Items**:
  - Set up connections to both networks.
  - Configure environment variables to switch between mainnet and testnet.
  - Test transactions on testnet before deploying to mainnet.

---

### **Testing, Deployment, and Marketing**

#### **4. Testing and Quality Assurance**

**4.1. Frontend and Backend Integration Testing**

- **Task**: Ensure seamless communication between frontend and backend.
- **Action Items**:
  - Test user flows: deposit, swap, memo inclusion.
  - Verify that transaction data is correctly stored and retrieved.
  - Check for edge cases and invalid inputs.

**4.2. Swap Transaction Testing**

- **Task**: Test swaps for multiple cryptocurrencies.
- **Action Items**:
  - Perform test swaps with various tokens on the testnet.
  - Ensure that swaps execute correctly and USDC is received.
  - Handle any swap failures or exceptions.

**4.3. Security Review**

- **Task**: Conduct a basic security review.
- **Action Items**:
  - Ensure that private keys and sensitive data are not exposed.
  - Validate user inputs to prevent injection attacks.
  - Review dependencies for known vulnerabilities.

#### **5. Deployment**

**5.1. Backend Deployment**

- **Task**: Deploy the Flask backend on Google Cloud.
- **Tools**: Google Cloud Run or Google App Engine.
- **Action Items**:
  - Containerize the Flask app using Docker.
  - Deploy the Docker container to Google Cloud Run.
  - Set up environment variables and secrets (API keys, database paths).
  - Test the deployed backend API endpoints.

**5.2. Database Deployment**

- **Task**: Deploy the SQLite database.
- **Action Items**:
  - For simplicity, package the SQLite database with the backend.
  - Ensure that the database file is correctly referenced in the deployed environment.
  - Consider using Google Cloud SQL if scalability is a concern.

**5.3. Frontend Deployment**

- **Task**: Deploy the React frontend.
- **Tools**: Vercel, Netlify, or Google Cloud Storage with Firebase Hosting.
- **Action Items**:
  - Build the React application (`npm run build`).
  - Deploy the build folder to the chosen hosting service.
  - Configure domain settings to point to the deployed frontend.
  - Ensure HTTPS is enabled for secure connections.

**5.4. Domain Linking**

- **Task**: Link your existing domain to the deployed website.
- **Action Items**:
  - Update DNS settings to point to the frontend hosting IP.
  - Configure DNS records (A, CNAME) as required.
  - Verify that the domain correctly resolves to the website.

#### **6. Final Adjustments**

**6.1. Enabling USDT Support**

- **Task**: Allow users to deposit USDT in addition to USDC.
- **Action Items**:
  - Update the frontend to include USDT as a deposit option.
  - Adjust backend validations to accept and process USDT transactions.
  - Test USDT deposits and swaps to USDC.

**6.2. User Data Display**

- **Task**: Enhance the frontend to display user-specific data.
- **Action Items**:
  - Create dashboard components to show:
    - Total funds deposited.
    - Lock duration and time remaining.
    - Transaction history.
  - Fetch data from the backend via API calls.
  - Ensure data is updated in real-time or at regular intervals.

#### **7. Marketing Setup**

**7.1. Social Media Presence**

- **Task**: Establish a Twitter account for the project.
- **Action Items**:
  - Create a new Twitter account with branding aligned to the project.
  - Design profile images and banners.
  - Write a compelling bio and pinned tweet explaining the project.

**7.2. Twitter Integration**

- **Task**: Automate marketing updates on Twitter.
- **Tools**: Twitter API v2, Tweepy (Python library).
- **Action Items**:
  - Set up a Twitter developer account and obtain API keys.
  - Write a script to post updates:
    - New deposits received.
    - Total funds locked milestones.
    - Countdown to project launch.
  - Schedule regular tweets or trigger them based on events.

**7.3. Website Integration**

- **Task**: Integrate Twitter feed into the website.
- **Action Items**:
  - Use Twitter's embedded timelines to display recent tweets.
  - Add social sharing buttons to encourage users to share.

---

### **Post-Deployment Considerations**

#### **8. Monitoring and Maintenance**

**8.1. Transaction Monitoring**

- **Task**: Ensure continuous monitoring of transactions.
- **Action Items**:
  - Set up alerts for any failures in transaction processing.
  - Monitor logs for any errors or exceptions.

**8.2. Database Backup**

- **Task**: Implement a backup strategy for the SQLite database.
- **Action Items**:
  - Schedule regular backups of the database file.
  - Store backups securely, possibly on Google Cloud Storage.

**8.3. Scalability Planning**

- **Task**: Prepare for increased user activity.
- **Action Items**:
  - Consider migrating from SQLite to a more robust database like PostgreSQL if needed.
  - Optimize code for performance.

---

### **Summary of Tools and Technologies**

- **Frontend**:
  - React.js
  - ethers.js
  - Uniswap SDK
  - Bybit Wallet SDK or alternatives
- **Backend**:
  - Python Flask
  - SQLite
  - Web3.py or ethers.js (Python)
  - Etherscan API
  - Tweepy (for Twitter integration)
- **Blockchain Interaction**:
  - ETH Mainnet/Testnet
  - Gnosis Safe SDK
  - Uniswap Protocol
- **Deployment**:
  - Google Cloud Platform
  - Docker
  - Vercel or Netlify (optional for frontend)
- **Marketing**:
  - Twitter API v2
  - Social media management tools (optional)

---

### **Risk Management and Contingency Plans**

- **Time Constraints**:

  - Prioritize core functionalities that must be completed within two days.
  - Optional features like Uniswap pool monitoring can be scheduled for after initial deployment.

- **Technical Challenges**:

  - **Uniswap Integration**: If difficulties arise, limit supported tokens to a smaller list where swaps are tested.
  - **Wallet Integration**: If Bybit Wallet integration is complex, consider using MetaMask or WalletConnect temporarily.

- **Testing**:
  - Allocate sufficient time on Day 2 for thorough testing.
  - Engage team members or friends to perform user acceptance testing.

---

### **Action Items Checklist**

**first step:**

- [ ] Set up React project and install dependencies.
- [ ] Design UI components and validate user inputs.
- [ ] Integrate wallet functionality.
- [ ] Implement Uniswap swap functionality in the frontend.
- [ ] Include memo in transactions.
- [ ] Set up Flask backend and SQLite database.
- [ ] Develop transaction monitoring script.
- [ ] Set up Gnosis Safe and collect signatory wallets.
- [ ] Configure ETH mainnet/testnet connections.

**second step:**

- [ ] Test frontend and backend integration.
- [ ] Perform swap transaction tests.
- [ ] Conduct security review.
- [ ] Deploy backend on Google Cloud.
- [ ] Deploy frontend and link domain.
- [ ] Enable USDT support.
- [ ] Enhance user data display on the frontend.
- [ ] Create Twitter account and set up branding.
- [ ] Implement Twitter automation scripts.
- [ ] Integrate Twitter feed into the website.
- [ ] Monitor and test the live application.
