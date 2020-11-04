pragma solidity ^0.5.11;

contract Auction{
    string public objectName;
    uint256 private bidDuration;
    uint256 public participatingCharge;
    uint256 private time;
    mapping (address => uint256) bids;
    uint256[] topBids;
    address winner;
    address payable[] bidders;
    address[] topBidders;
    
    
    constructor(string memory _objectName, uint256 _bidDuration) public {
        objectName = _objectName;
        bidDuration = now + _bidDuration*(1 minutes);
        participatingCharge = 2 ether;
        for(uint8 i=0; i<6;i++){
            topBids.push(0);
            topBidders.push(0x0000000000000000000000000000000000000000);
        }
        }
    
    // is bidder a participant?
    function isParticipant(address addr) private view returns(bool){
        bool flag = false;
        for(uint8 i = 0 ; i < bidders.length ; i++){
            if(addr == bidders[i]){
                flag = true;
            }
        }
        return flag;
    }     
    
    // is Bid active?
    function isBidActive() public view returns(bool){
        if(bidDuration > now){
            return true;
        }
        else{
            return false;
        }
    }
    
    function check(address sender) private returns (bool){
        for(uint8 i=0;i<topBidders.length;i++){
            if(sender==topBidders[i]){
                topBids[i]=0;
                topBidders[i]=0x0000000000000000000000000000000000000000;
                return true;
            }
        }
        return false;
    }
    // store top 5 bidding amount
    function insert(address sender,uint256 val) private{
            uint256 temp;
            address temp_addr;
            check(sender);
            for(uint8 i=0;i<6;i++){
                if(topBids[i]<val){
                    temp=topBids[i];
                    topBids[i]=val;
                    val=temp;
                    temp_addr=topBidders[i];
                    topBidders[i]=sender;
                    sender=temp_addr;
                }
            }
    }
    
    // participate before bidding and pay participating Charge
    function participate() public payable{
        require(isBidActive(), "Bid has ended");
        require(!isParticipant(msg.sender), "You are already a participant");
        require(msg.value == participatingCharge);
        bidders.push(msg.sender);
    }
    
    // place bids and pay a security deposit .
    // to check the security deposit amount use calculateSecurityAmount
    function placeBid(uint256 bidAmount) public payable {
        require(isParticipant(msg.sender), "You are not participant. Please first participate");
        require(isBidActive(), "Bid has ended.");
        uint256 bidAm=bidAmount/10;
        require( msg.value>= bidAm*(1 ether), "Please pay 10% of your bidAmount as security deposit");
        bids[msg.sender] += bidAmount*(1 ether);
        insert(msg.sender,bids[msg.sender]);
        
    }
    
    // view top 5 bids
    function viewBids() public view returns(uint256[] memory){
        return topBids;
    }
    
    // view my bids
    function viewMyBid() public view returns (uint256){
        return bids[msg.sender];
    }
    
    // calculate Security Amount
    function calculateSecurityAmount(uint256 bidAmount) public pure returns(uint256){
        return bidAmount/10;
    }
    
    // view the result only after auction ends
    function viewResult() public returns(address){
        require(bidDuration<now, "Auction is active");
        for(uint8 i=0; i<bidders.length; i++){
            if(bids[bidders[i]] == topBids[0]){
                winner = bidders[i];
                break;
            }
        }
        return winner;
    }
    
    // pay amount to contract and refund the security deposit of all bidders
    function payAmount() public payable{
        require(bidDuration<now,"Auction is active");
        require(winner == msg.sender,"You are not winner");
        require(bids[msg.sender]==msg.value, "Incorrect amount");
        for(uint8 i=0 ;i<bidders.length; i++){
            uint256 securityDeposit = bids[bidders[i]]/10;
            bidders[i].transfer(securityDeposit);
        }
    }
    
    function withdrawBid() public{
        require(isParticipant(msg.sender), "You are not a participant");
        bids[msg.sender] = 0;
        if(topBidders[0]==msg.sender){
        for(uint8 i=1; i<6; i++){
                topBids[i-1] = topBids[i];
                topBidders[i-1] = topBidders[i];
            }
        topBids[5]=0;
        topBidders[5]=0x0000000000000000000000000000000000000000;
        }
        }
     
}