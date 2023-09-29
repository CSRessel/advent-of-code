fn parse(input: &str) -> Option<Vec<u32>> {
    // stack representing the hierarchy of the current working directory
    let mut dir_stack: Vec<u32> = Vec::new();
    // list of directories we have completely finished sizing
    let mut dir_explored: Vec<u32> = Vec::new();

    // iterating line by line
    for line in input.lines() {
        match line.split_whitespace().collect::<Vec<&str>>().as_slice() {
            // skip these cases, because dir names are irrelevant
            ["dir", _] => (),
            ["$", "ls"] => (),
            // add the current dir size to the explored dirs
            // (because in the input, we never revisit dirs)
            ["$", "cd", ".."] => if let Some(dir_previous) = dir_stack.pop() {
                    dir_explored.push(dir_previous)
                } else {
                    println!("Trying to cd parent from root!");
                    return None;
                },
            // directory entered doesn't matter, because each size is counted
            // against every parent dir for the current dir_stack
            // (and in the input, we only navigate to each subdir once, so
            // dir names don't really matter)
            ["$", "cd", _] => dir_stack.push(0),
            // add the current file size to every parent dir for the current
            // dir_stack because it counts for all their sizes
            [size, _] => if let Ok(num_size) = size.parse::<u32>() {
                    dir_stack.iter_mut().for_each(|d| *d += num_size);
                } else {
                    println!("Unrecognized input! Line: {0}", size);
                    return None;
                },
            [..] => {
                    println!("Empty line!");
                    return None;
                }
        }
    }

    // because we don't cd up from wherever we ended, just add all the dirs
    // left in the dir stack to the explored
    dir_explored.extend(dir_stack);
    return Some(dir_explored);
}

pub fn part_one(input: &str) -> Option<u32> {
    // option monad :)
    return parse(input).map(|dir_explored| {
        return dir_explored
            .iter()
            .filter(|&&dir_size| dir_size < 100_000)
            .sum();
    });
}

pub fn part_two(input: &str) -> Option<u32> {
    return parse(input).and_then(|mut dir_explored| {
        dir_explored.sort_unstable();
        let root_size: u32 = *dir_explored.last().unwrap();
        let min_space_needed: u32 = root_size + 30_000_000 - 70_000_000;
        return dir_explored
            .iter()
            .find(|&&dir_size| dir_size >= min_space_needed)
            .map(|&min_deletion| min_deletion);
        // I can't figure out why this ends up being a reference,
        // is it just because it's going into the Option?
    });
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 7);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 7);
        assert_eq!(part_one(&input), Some(95437));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 7);
        assert_eq!(part_two(&input), Some(24933642));
    }
}
