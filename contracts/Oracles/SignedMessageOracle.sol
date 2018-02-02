pragma solidity ^0.4.18;
import "../Oracles/Oracle.sol";
import "../Utils/Proxy.sol";


contract SignedMessageOracleData {

    /*
     *  Events
     */
    event SignerReplacement(address indexed newSigner);
    event OutcomeAssignment(int outcome);

    /*
     *  Storage
     */
    address public signer;
    bytes32 public descriptionHash;
    uint nonce;
    bool public isSet;
    int public outcome;

    /*
     *  Modifiers
     */
    modifier isSigner () {
        // Only signer is allowed to proceed
        require(msg.sender == signer);
        _;
    }
}

contract SignedMessageOracleProxy is Proxy, SignedMessageOracleData {

    /// @dev Constructor sets signer address based on signature
    /// @param _descriptionHash Hash identifying off chain event description
    /// @param v Signature parameter
    /// @param r Signature parameter
    /// @param s Signature parameter
    function SignedMessageOracleProxy(address proxied, bytes32 _descriptionHash, uint8 v, bytes32 r, bytes32 s)
        Proxy(proxied)
        public
    {
        signer = ecrecover(_descriptionHash, v, r, s);
        descriptionHash = _descriptionHash;
    }
}

/// @title Signed message oracle contract - Allows to set an outcome with a signed message
/// @author Stefan George - <stefan@gnosis.pm>
contract SignedMessageOracle is Proxied, Oracle, SignedMessageOracleData {

    /*
     *  Public functions
     */
    /// @dev Replaces signer
    /// @param newSigner New signer
    /// @param _nonce Unique nonce to prevent replay attacks
    /// @param v Signature parameter
    /// @param r Signature parameter
    /// @param s Signature parameter
    function replaceSigner(address newSigner, uint _nonce, uint8 v, bytes32 r, bytes32 s)
        public
        isSigner
    {
        // Result is not set yet and nonce and signer are valid
        require(   !isSet
                && _nonce > nonce
                && signer == ecrecover(keccak256(descriptionHash, newSigner, _nonce), v, r, s));
        nonce = _nonce;
        signer = newSigner;
        SignerReplacement(newSigner);
    }

    /// @dev Sets outcome based on signed message
    /// @param _outcome Signed event outcome
    /// @param v Signature parameter
    /// @param r Signature parameter
    /// @param s Signature parameter
    function setOutcome(int _outcome, uint8 v, bytes32 r, bytes32 s)
        public
    {
        // Result is not set yet and signer is valid
        require(   !isSet
                && signer == ecrecover(keccak256(descriptionHash, _outcome), v, r, s));
        isSet = true;
        outcome = _outcome;
        OutcomeAssignment(_outcome);
    }

    /// @dev Returns if winning outcome
    /// @return Is outcome set?
    function isOutcomeSet()
        public
        view
        returns (bool)
    {
        return isSet;
    }

    /// @dev Returns winning outcome
    /// @return Outcome
    function getOutcome()
        public
        view
        returns (int)
    {
        return outcome;
    }
}
