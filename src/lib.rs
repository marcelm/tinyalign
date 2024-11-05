use pyo3::exceptions::PyIndexError;
use pyo3::prelude::*;

/// Return the edit distance between the strings s and t.
/// The edit distance is the sum of the numbers of insertions, deletions,
/// and mismatches that is minimally necessary to transform one string
/// into the other.
///
/// If maxdiff is not -1, then a banded alignment is performed. In that case,
/// the true edit distance is returned if and only if it is maxdiff or less.
/// Otherwise, a value is returned that is guaranteed to be greater than
/// maxdiff, but which is not necessarily the true edit distance.
#[pyfunction]
#[pyo3(signature=(s, t, maxdiff=-1))]
pub fn edit_distance(s: &str, t: &str, maxdiff: i64) -> PyResult<usize> {
    let s = s.as_bytes();
    let t = t.as_bytes();
    //let m = s.len();  // index: i
    //let n = t.len();  // index: j

    let maxdiff = if maxdiff < 0 { None } else { Some(maxdiff as usize) };

    // Return early if string lengths are too different
    let absdiff = s.len().abs_diff(t.len());
    if let Some(e) = maxdiff {
        if absdiff > e {
            return Ok(absdiff);
        }
    }

    // let s_range = 0..s.len();
    // let t_range = 0..t.len();

    // Skip identical prefixes
    let common_prefix_length = if let Some(pos) = s.iter().zip(t.iter()).position(|(c, d)| c != d) {
        pos
    } else {
        // One string is a prefix of the other
        return Ok(absdiff);
    };
    let s = &s[common_prefix_length..];
    let t = &t[common_prefix_length..];

    // Skip identical suffixes
    // # Skip identical suffixes
    // while m > 0 and n > 0 and sv[m-1] == tv[n-1]:
    //     m -= 1
    // n -= 1
    // let s_end = s.len();
    // let t_end = t.len();
    // while s.len() > 0 && t.len() > 0 && s[s.len() - 1] == t[t.len() - 1] {
    //
    // }

    let mut costs = (0..=s.len()).collect::<Vec<_>>();

    if maxdiff.is_none() {
        // Regular (unbanded) global alignment
        let mut prev;
        for j in 1..=t.len() {
            prev = costs[0];
            costs[0] += 1;
            for i in 1..=s.len() {
                let equals = s[i - 1] == t[j - 1];
                let c = *[1 + prev - equals as usize, 1 + costs[i], 1 + costs[i - 1]].iter().min().unwrap();
                prev = costs[i];
                costs[i] = c;
            }
        }

        Ok(costs[s.len()])
    } else {
        // Banded alignment
        let e = maxdiff.unwrap();
        let mut smallest = 0;
        for j in 1..=t.len() {
            let stop = *[j + e + 1, s.len() + 1].iter().min().unwrap();
            let mut prev;
            let start;
            if j <= e {
                prev = costs[0];
                costs[0] += 1;
                smallest = costs[0];
                start = 1;
            } else {
                start = j - e;
                prev = costs[start - 1];
                smallest = e + 1;
            }
            for i in start..stop {
                let equals = s[i - 1] == t[j - 1];
                let c = *[
                    1 + prev - equals as usize,
                    1 + costs[i],
                    1 + costs[i - 1],
                ].iter().min().unwrap();
                prev = costs[i];
                costs[i] = c;
                smallest = smallest.min(c);
            }
            if smallest > e {
                break;
            }
        }

        if smallest > e {
            Ok(smallest)
        } else {
            Ok(costs[s.len()])
        }
    }
}

/// Compute hamming distance between two strings. If they do not have the
/// same length, an IndexError is raised.
///
/// Return the number of differences between the strings.
#[pyfunction]
pub fn hamming_distance(s: &str, t: &str) -> PyResult<u64> {
    if s.len() != t.len() {
        return Err(PyIndexError::new_err("sequences must have the same length"));
    }
    Ok(s.chars().zip(t.chars()).map(|(c, d)| if c != d { 1 } else { 0 }).sum())
}


#[pymodule]
fn tinyalign(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(edit_distance, m)?)?;
    m.add_function(wrap_pyfunction!(hamming_distance, m)?)?;
    Ok(())
}


/*
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}*/
