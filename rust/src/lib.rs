// extern libc;

#[no_mangle]
pub extern fn test() {
    println!("test from rust...")
}


#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        test();
    }
}
