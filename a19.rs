// if you'd like to run this code the following dependencies are required
// (create a new project with `cargo new` and edit Cargo.toml)
// [dependencies]
// nalgebra = "0.29"
// itertools = "0.10.2"
use itertools::Itertools;
use nalgebra::{Matrix3, Point3, Vector3};
use std::collections::{HashMap, HashSet};

type Point = Point3<i16>;
type Vector = Vector3<i16>;
type Matrix = Matrix3<i16>;
type Distances = HashMap<Point, HashSet<i16>>;

fn generate_orientations() -> Vec<Matrix> {
    let mut result = Vec::with_capacity(24);
    for x in [-1, 1] {
        for y in [-1, 1] {
            for indexes in (0..3).permutations(3) {
                let mut x_axis = Vector::zeros();
                x_axis[indexes[0]] = x;

                let mut y_axis = Vector::zeros();
                y_axis[indexes[1]] = y;

                // the z axis is always the result of x.cross(y), this way we don't have invalid orientations
                let z_axis = x_axis.cross(&y_axis);

                let orientation = Matrix::from_columns(&[x_axis, y_axis, z_axis]);
                result.push(orientation);
            }
        }
    }
    result
}

fn transform(point: &Point, orientation: &Matrix, translation: &Vector) -> Point {
    orientation * point + translation
}

fn manhattan_distance(p1: &Point, p2: &Point) -> i16 {
    (p1 - p2).into_iter().map(|n| n.abs()).sum()
}

fn distances(beacons: &HashSet<Point>) -> Distances {
    let mut result = Distances::with_capacity(beacons.len());
    for beacon1 in beacons {
        let mut d = HashSet::new();
        for beacon2 in beacons {
            d.insert(manhattan_distance(beacon1, beacon2));
        }
        result.insert(beacon1.to_owned(), d);
    }
    result
}

fn parse(text: &str) -> Vec<HashSet<Point>> {
    let mut result = Vec::new();

    for beacon_text in text.split("\n\n") {
        let mut beacon = HashSet::new();
        for line in beacon_text.split('\n').skip(1) {
            let mut point = Point::origin();
            for (idx, num_text) in line.split(',').enumerate() {
                point[idx] = num_text.parse().unwrap();
            }
            beacon.insert(point);
        }
        result.push(beacon);
    }

    result
}

fn find_center_pair(
    origin_distances: Distances,
    beacon_distances: &[Distances],
) -> Option<(Point, Point, usize)> {
    for (center1, distances1) in origin_distances {
        for (idx, scanner) in beacon_distances.iter().enumerate() {
            for (center2, distances2) in scanner {
                // since two points have 12 identical distances to other points in the same coordinate system
                // we can reasonably assume these are the same point
                if distances1.intersection(distances2).count() >= 12 {
                    return Some((center1, center2.to_owned(), idx));
                }
            }
        }
    }
    None
}

fn match_orientation(
    set1: &HashSet<Point>,
    set2: &HashSet<Point>,
    center1: Point,
    center2: Point,
    orientations: &[Matrix],
) -> Option<(Point, HashSet<Point>)> {
    for orientation in orientations {
        let modified_center2 = orientation * center2;

        // this translation will result in center2 = center1
        // now we have to apply this to all other data points and see if it's a match
        let translation = center1 - modified_center2;
        let transformed_set2: HashSet<Point> = set2
            .iter()
            .map(|p| transform(p, orientation, &translation))
            .collect();
        if set1.intersection(&transformed_set2).count() >= 12 {
            return Some((translation.into(), transformed_set2));
        }
    }

    None
}

fn geolocate(mut beacons: Vec<HashSet<Point>>) -> (HashSet<Point>, Vec<Point>) {
    let mut beacon_locations = vec![Point::new(0, 0, 0)];
    let mut around_origin = beacons.remove(0);

    let mut beacon_distances = beacons.iter().map(distances).collect::<Vec<_>>();

    let orientations = generate_orientations();

    while !beacons.is_empty() {
        let origin_distances = distances(&around_origin);
        let (center1, center2, idx) =
            find_center_pair(origin_distances, &beacon_distances).unwrap();
        let (real_center2, new_points) = match_orientation(
            &around_origin,
            &beacons[idx],
            center1,
            center2,
            &orientations,
        )
        .unwrap();
        around_origin.extend(new_points);
        beacon_locations.push(real_center2);

        beacon_distances.remove(idx);
        beacons.remove(idx);
    }

    (around_origin, beacon_locations)
}

fn max_mh(scanner_locations: Vec<Point>) -> i16 {
    scanner_locations
        .iter()
        .enumerate()
        .flat_map(|(idx, p1)| {
            scanner_locations
                .iter()
                .skip(idx + 1)
                .map(|p2| manhattan_distance(p1, p2))
        })
        .max()
        .unwrap()
}

use std::env;
use std::fs::File;
use std::io::prelude::*;

fn main() -> std::io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Error: argument count mismatch, expected 1, found {}\nProvide a scanner file as the only argument.", args.len() - 1);
        return Ok(());
    }

    let mut file = File::open(&args[1])?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let beacons = parse(&contents);
    let (all_beacons, scanner_locations) = geolocate(beacons);
    println!("Part 1: {}", all_beacons.len());
    println!("Part 2: {}", max_mh(scanner_locations));

    Ok(())
}
