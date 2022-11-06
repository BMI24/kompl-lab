#![allow(dead_code)]

use clap::Parser;
use std::io::{self, BufRead};
use std::collections::HashMap;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Cli {
    name:String,
    #[arg(short, long)]
    verbose: bool,
}

enum State {
    Yes,
    No,
    Halt,
    NumberedState{x : i32}
}

enum TapeSymbol {
    Start,
    Empty,
    Zero,
    One
}

struct MachineState {
    tape : Vec<TapeSymbol>,
    state : State,
    head_position : usize
}

struct InputData{
    action_map : HashMap<(i32, i32), i32>,
    input : Vec<TapeSymbol>
}

enum InputParseError{
    CliParseError(std::io::Error),
    ParseIntError(std::num::ParseIntError),
    NotSupported
}

impl From<std::io::Error> for InputParseError{
    fn from(err: std::io::Error) -> Self {
        Self::CliParseError(err)
    }
}

impl From<std::num::ParseIntError> for InputParseError{
    fn from(err: std::num::ParseIntError) -> Self {
        Self::ParseIntError(err)
    }
}

fn read_input_data() -> Result<InputData, InputParseError> {
    let stdin = io::stdin();
    struct FirstLineData{
        state_count : i32,
        transitions_count : i32
    }
    let mut first_line_data:Option<FirstLineData> = None;
    for line_result in stdin.lock().lines() {
        let line:String = line_result?;
        if first_line_data.is_none(){
            let line_split:Vec<&str> = line.split(' ').collect();
            let state_count: i32 = line_split[0].parse()?;
            let transitions_count: i32 = line_split[1].parse()?;
            first_line_data = Some(FirstLineData{state_count, transitions_count});
        }
        else {
            let data = first_line_data.unwrap();
        }
    }

    return Ok(InputData{action_map:HashMap::new(), input:vec![]});
}

fn main() {
    
}