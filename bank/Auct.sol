pragma solidity ^0.5.11;
contract Auct
{
    mapping (address => uint256) bid;
    address[10] public participant;
    address public topBidder;
    uint256 public n_participants = 0;
    uint256 public ended = 0; 
    
    constructor() public{
        
    }
    function isEnded() public view returns(uint256)
    {
        return ended;
    }
    function setEnd() public
    {
        ended = 1;
    }
    function placeBid(address addr, uint256 bidAmt) public
    {
        participant[n_participants] = addr;
        bid[addr] = bidAmt;
        n_participants += 1;
        uint256 maxx = bid[participant[0]];
        topBidder = participant[0];
        for(uint256 i=1;i<n_participants;i++)
        {
            
            if(bid[participant[i]] > maxx)
            {
                topBidder = participant[i];
                maxx = bid[participant[i]];
            }
        }
    }
    function get_n_participants() public view returns(uint256)
    {
        return n_participants;
    }
    function viewBids(uint256 i) public view returns(address)
    {
        return participant[i]; 
    }
    function getBids(address addr) public view returns(uint256)
    {
        return bid[addr];
    }
    function getTopBidder() public view returns(address)
    {
        return topBidder;
    }
    function withdraw(address addr) public 
    {
        uint256 flag=0;
        for(uint256 i=0;i<n_participants;i++)
        {
            if(flag==1)
            {
                participant[i-1] = participant[i];
            }
            else
            {
                if(participant[i]==addr)
                {
                    flag=1;
                }
            }
        }
        n_participants -= 1;
        uint256 maxx = bid[participant[0]];
        topBidder = participant[0];
        for(uint256 i=1;i<n_participants;i++)
        {
            
            if(bid[participant[i]] > maxx)
            {
                topBidder = participant[i];
                maxx = bid[participant[i]];
            }
        }
    }
}