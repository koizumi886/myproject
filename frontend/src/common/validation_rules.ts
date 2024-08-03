
const require_rule = 
    (value: string) => {
      if (value) return true;
  
      return "This is required.";
    };

    
    
function maxLength_rule(len :number) {
    const str =(value: string) => {
        if (value?.length <= len) return true;
    
        return `This must be less than ${len} characters.`;
        };
    return str;
    }


  export { require_rule, maxLength_rule };