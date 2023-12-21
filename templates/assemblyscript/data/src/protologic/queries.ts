// DO NOT MODIFY, THIS FILE IS GENERATED //
// VERSION 0.2.0 //

import {Vector3} from "./Vector3";
import {Quaternion} from "./Quaternion";
import {RadarTargetInfo} from "./RadarTargetInfo";
import {RadarContactInfo} from "./RadarContactInfo";


// queries.ts


// @ts-ignore
@external("protologic", "cpu_get_fuel")
declare function _internal_cpu_get_fuel(): i64;

/**
 */
export function cpu_get_fuel(): i64 {
	return _internal_cpu_get_fuel();
}

// @ts-ignore
@external("protologic", "ship_get_position_x")
declare function _internal_ship_get_position_x(): f32;

/**
 */
export function ship_get_position_x(): f32 {
	return _internal_ship_get_position_x();
}

// @ts-ignore
@external("protologic", "ship_get_position_y")
declare function _internal_ship_get_position_y(): f32;

/**
 */
export function ship_get_position_y(): f32 {
	return _internal_ship_get_position_y();
}

// @ts-ignore
@external("protologic", "ship_get_position_z")
declare function _internal_ship_get_position_z(): f32;

/**
 */
export function ship_get_position_z(): f32 {
	return _internal_ship_get_position_z();
}

// @ts-ignore
@external("protologic", "ship_get_position_ptr")
declare function _internal_ship_get_position_ptr(dst: Vector3): void;

/**
 */
export function ship_get_position_ptr(dst: Vector3): void {
	return _internal_ship_get_position_ptr(dst);
}

// @ts-ignore
@external("protologic", "ship_get_velocity_x")
declare function _internal_ship_get_velocity_x(): f32;

/**
 */
export function ship_get_velocity_x(): f32 {
	return _internal_ship_get_velocity_x();
}

// @ts-ignore
@external("protologic", "ship_get_velocity_y")
declare function _internal_ship_get_velocity_y(): f32;

/**
 */
export function ship_get_velocity_y(): f32 {
	return _internal_ship_get_velocity_y();
}

// @ts-ignore
@external("protologic", "ship_get_velocity_z")
declare function _internal_ship_get_velocity_z(): f32;

/**
 */
export function ship_get_velocity_z(): f32 {
	return _internal_ship_get_velocity_z();
}

// @ts-ignore
@external("protologic", "ship_get_velocity_ptr")
declare function _internal_ship_get_velocity_ptr(dst: Vector3): void;

/**
 */
export function ship_get_velocity_ptr(dst: Vector3): void {
	return _internal_ship_get_velocity_ptr(dst);
}

// @ts-ignore
@external("protologic", "ship_get_orientation_x")
declare function _internal_ship_get_orientation_x(): f32;

/**
 */
export function ship_get_orientation_x(): f32 {
	return _internal_ship_get_orientation_x();
}

// @ts-ignore
@external("protologic", "ship_get_orientation_y")
declare function _internal_ship_get_orientation_y(): f32;

/**
 */
export function ship_get_orientation_y(): f32 {
	return _internal_ship_get_orientation_y();
}

// @ts-ignore
@external("protologic", "ship_get_orientation_z")
declare function _internal_ship_get_orientation_z(): f32;

/**
 */
export function ship_get_orientation_z(): f32 {
	return _internal_ship_get_orientation_z();
}

// @ts-ignore
@external("protologic", "ship_get_orientation_w")
declare function _internal_ship_get_orientation_w(): f32;

/**
 */
export function ship_get_orientation_w(): f32 {
	return _internal_ship_get_orientation_w();
}

// @ts-ignore
@external("protologic", "ship_get_orientation_ptr")
declare function _internal_ship_get_orientation_ptr(dst: Quaternion): void;

/**
 */
export function ship_get_orientation_ptr(dst: Quaternion): void {
	return _internal_ship_get_orientation_ptr(dst);
}

// @ts-ignore
@external("protologic", "ship_get_angularvelocity_x")
declare function _internal_ship_get_angularvelocity_x(): f32;

/**
 */
export function ship_get_angularvelocity_x(): f32 {
	return _internal_ship_get_angularvelocity_x();
}

// @ts-ignore
@external("protologic", "ship_get_angularvelocity_y")
declare function _internal_ship_get_angularvelocity_y(): f32;

/**
 */
export function ship_get_angularvelocity_y(): f32 {
	return _internal_ship_get_angularvelocity_y();
}

// @ts-ignore
@external("protologic", "ship_get_angularvelocity_z")
declare function _internal_ship_get_angularvelocity_z(): f32;

/**
 */
export function ship_get_angularvelocity_z(): f32 {
	return _internal_ship_get_angularvelocity_z();
}

// @ts-ignore
@external("protologic", "ship_get_angularvelocity_ptr")
declare function _internal_ship_get_angularvelocity_ptr(dst: Vector3): void;

/**
 */
export function ship_get_angularvelocity_ptr(dst: Vector3): void {
	return _internal_ship_get_angularvelocity_ptr(dst);
}

// @ts-ignore
@external("protologic", "engine_get_fuel_amount")
declare function _internal_engine_get_fuel_amount(): f32;

/**
 */
export function engine_get_fuel_amount(): f32 {
	return _internal_engine_get_fuel_amount();
}

// @ts-ignore
@external("protologic", "engine_get_fuel_capacity")
declare function _internal_engine_get_fuel_capacity(): f32;

/**
 */
export function engine_get_fuel_capacity(): f32 {
	return _internal_engine_get_fuel_capacity();
}

// @ts-ignore
@external("protologic", "engine_get_throttle")
declare function _internal_engine_get_throttle(): f32;

/**
 */
export function engine_get_throttle(): f32 {
	return _internal_engine_get_throttle();
}

// @ts-ignore
@external("protologic", "radar_get_target_count")
declare function _internal_radar_get_target_count(): i32;

/**
 * @deprecated
 */
export function radar_get_target_count(): i32 {
	return _internal_radar_get_target_count();
}

// @ts-ignore
@external("protologic", "radar_get_target_distance")
declare function _internal_radar_get_target_distance(index: i32): f32;

/**
 * @deprecated
 */
export function radar_get_target_distance(index: i32): f32 {
	return _internal_radar_get_target_distance(index);
}

// @ts-ignore
@external("protologic", "radar_get_target_type")
declare function _internal_radar_get_target_type(index: i32): i32;

/**
 * @deprecated
 */
export function radar_get_target_type(index: i32): i32 {
	return _internal_radar_get_target_type(index);
}

// @ts-ignore
@external("protologic", "radar_get_target_id")
declare function _internal_radar_get_target_id(index: i32): i64;

/**
 * @deprecated
 */
export function radar_get_target_id(index: i32): i64 {
	return _internal_radar_get_target_id(index);
}

// @ts-ignore
@external("protologic", "radar_get_target_info")
declare function _internal_radar_get_target_info(index: i32, ptr: RadarTargetInfo): void;

/**
 * @deprecated
 */
export function radar_get_target_info(index: i32, ptr: RadarTargetInfo): void {
	return _internal_radar_get_target_info(index, ptr);
}

// @ts-ignore
@external("protologic", "radar_get_target_list")
declare function _internal_radar_get_target_list(ptr: RadarTargetInfo, len: i32): void;

/**
 * @deprecated
 */
export function radar_get_target_list(ptr: RadarTargetInfo, len: i32): void {
	return _internal_radar_get_target_list(ptr, len);
}

// @ts-ignore
@external("protologic", "radar_get_noise")
declare function _internal_radar_get_noise(): f32;

/**
 */
export function radar_get_noise(): f32 {
	return _internal_radar_get_noise();
}

// @ts-ignore
@external("protologic", "radar_get_contact_count")
declare function _internal_radar_get_contact_count(): i32;

/**
 */
export function radar_get_contact_count(): i32 {
	return _internal_radar_get_contact_count();
}

// @ts-ignore
@external("protologic", "radar_get_contact_type")
declare function _internal_radar_get_contact_type(index: i32): i32;

/**
 */
export function radar_get_contact_type(index: i32): i32 {
	return _internal_radar_get_contact_type(index);
}

// @ts-ignore
@external("protologic", "radar_get_contact_id")
declare function _internal_radar_get_contact_id(index: i32): i64;

/**
 */
export function radar_get_contact_id(index: i32): i64 {
	return _internal_radar_get_contact_id(index);
}

// @ts-ignore
@external("protologic", "radar_get_contact_strength")
declare function _internal_radar_get_contact_strength(index: i32): f32;

/**
 */
export function radar_get_contact_strength(index: i32): f32 {
	return _internal_radar_get_contact_strength(index);
}

// @ts-ignore
@external("protologic", "radar_get_contact_position_x")
declare function _internal_radar_get_contact_position_x(index: i32): f32;

/**
 */
export function radar_get_contact_position_x(index: i32): f32 {
	return _internal_radar_get_contact_position_x(index);
}

// @ts-ignore
@external("protologic", "radar_get_contact_position_y")
declare function _internal_radar_get_contact_position_y(index: i32): f32;

/**
 */
export function radar_get_contact_position_y(index: i32): f32 {
	return _internal_radar_get_contact_position_y(index);
}

// @ts-ignore
@external("protologic", "radar_get_contact_position_z")
declare function _internal_radar_get_contact_position_z(index: i32): f32;

/**
 */
export function radar_get_contact_position_z(index: i32): f32 {
	return _internal_radar_get_contact_position_z(index);
}

// @ts-ignore
@external("protologic", "radar_get_contact_position_ptr")
declare function _internal_radar_get_contact_position_ptr(index: i32, dst: Vector3): void;

/**
 */
export function radar_get_contact_position_ptr(index: i32, dst: Vector3): void {
	return _internal_radar_get_contact_position_ptr(index, dst);
}

// @ts-ignore
@external("protologic", "radar_get_contact_info")
declare function _internal_radar_get_contact_info(index: i32, dst: RadarContactInfo): void;

/**
 */
export function radar_get_contact_info(index: i32, dst: RadarContactInfo): void {
	return _internal_radar_get_contact_info(index, dst);
}

// @ts-ignore
@external("protologic", "radar_get_contact_list")
declare function _internal_radar_get_contact_list(ptr: RadarContactInfo, len: i32): void;

/**
 */
export function radar_get_contact_list(ptr: RadarContactInfo, len: i32): void {
	return _internal_radar_get_contact_list(ptr, len);
}

// @ts-ignore
@external("protologic", "gun0_get_bearing")
declare function _internal_gun0_get_bearing(): f32;

/**
 */
export function gun0_get_bearing(): f32 {
	return _internal_gun0_get_bearing();
}

// @ts-ignore
@external("protologic", "gun0_get_elevation")
declare function _internal_gun0_get_elevation(): f32;

/**
 */
export function gun0_get_elevation(): f32 {
	return _internal_gun0_get_elevation();
}

// @ts-ignore
@external("protologic", "gun0_get_refiretime")
declare function _internal_gun0_get_refiretime(): f32;

/**
 */
export function gun0_get_refiretime(): f32 {
	return _internal_gun0_get_refiretime();
}

// @ts-ignore
@external("protologic", "gun0_get_magazine_capacity")
declare function _internal_gun0_get_magazine_capacity(): i32;

/**
 */
export function gun0_get_magazine_capacity(): i32 {
	return _internal_gun0_get_magazine_capacity();
}

// @ts-ignore
@external("protologic", "gun0_get_magazine_remaining")
declare function _internal_gun0_get_magazine_remaining(): i32;

/**
 */
export function gun0_get_magazine_remaining(): i32 {
	return _internal_gun0_get_magazine_remaining();
}

// @ts-ignore
@external("protologic", "gun0_get_magazine_type")
declare function _internal_gun0_get_magazine_type(): i32;

/**
 */
export function gun0_get_magazine_type(): i32 {
	return _internal_gun0_get_magazine_type();
}

// @ts-ignore
@external("protologic", "gun0_get_magazine_reloadtime")
declare function _internal_gun0_get_magazine_reloadtime(): f32;

/**
 */
export function gun0_get_magazine_reloadtime(): f32 {
	return _internal_gun0_get_magazine_reloadtime();
}

// @ts-ignore
@external("protologic", "gun1_get_bearing")
declare function _internal_gun1_get_bearing(): f32;

/**
 */
export function gun1_get_bearing(): f32 {
	return _internal_gun1_get_bearing();
}

// @ts-ignore
@external("protologic", "gun1_get_elevation")
declare function _internal_gun1_get_elevation(): f32;

/**
 */
export function gun1_get_elevation(): f32 {
	return _internal_gun1_get_elevation();
}

// @ts-ignore
@external("protologic", "gun1_get_refiretime")
declare function _internal_gun1_get_refiretime(): f32;

/**
 */
export function gun1_get_refiretime(): f32 {
	return _internal_gun1_get_refiretime();
}

// @ts-ignore
@external("protologic", "gun1_get_magazine_capacity")
declare function _internal_gun1_get_magazine_capacity(): i32;

/**
 */
export function gun1_get_magazine_capacity(): i32 {
	return _internal_gun1_get_magazine_capacity();
}

// @ts-ignore
@external("protologic", "gun1_get_magazine_remaining")
declare function _internal_gun1_get_magazine_remaining(): i32;

/**
 */
export function gun1_get_magazine_remaining(): i32 {
	return _internal_gun1_get_magazine_remaining();
}

// @ts-ignore
@external("protologic", "gun1_get_magazine_type")
declare function _internal_gun1_get_magazine_type(): i32;

/**
 */
export function gun1_get_magazine_type(): i32 {
	return _internal_gun1_get_magazine_type();
}

// @ts-ignore
@external("protologic", "gun1_get_magazine_reloadtime")
declare function _internal_gun1_get_magazine_reloadtime(): f32;

/**
 */
export function gun1_get_magazine_reloadtime(): f32 {
	return _internal_gun1_get_magazine_reloadtime();
}

// @ts-ignore
@external("protologic", "gun2_get_bearing")
declare function _internal_gun2_get_bearing(): f32;

/**
 */
export function gun2_get_bearing(): f32 {
	return _internal_gun2_get_bearing();
}

// @ts-ignore
@external("protologic", "gun2_get_elevation")
declare function _internal_gun2_get_elevation(): f32;

/**
 */
export function gun2_get_elevation(): f32 {
	return _internal_gun2_get_elevation();
}

// @ts-ignore
@external("protologic", "gun2_get_refiretime")
declare function _internal_gun2_get_refiretime(): f32;

/**
 */
export function gun2_get_refiretime(): f32 {
	return _internal_gun2_get_refiretime();
}

// @ts-ignore
@external("protologic", "gun2_get_magazine_capacity")
declare function _internal_gun2_get_magazine_capacity(): i32;

/**
 */
export function gun2_get_magazine_capacity(): i32 {
	return _internal_gun2_get_magazine_capacity();
}

// @ts-ignore
@external("protologic", "gun2_get_magazine_remaining")
declare function _internal_gun2_get_magazine_remaining(): i32;

/**
 */
export function gun2_get_magazine_remaining(): i32 {
	return _internal_gun2_get_magazine_remaining();
}

// @ts-ignore
@external("protologic", "gun2_get_magazine_type")
declare function _internal_gun2_get_magazine_type(): i32;

/**
 */
export function gun2_get_magazine_type(): i32 {
	return _internal_gun2_get_magazine_type();
}

// @ts-ignore
@external("protologic", "gun2_get_magazine_reloadtime")
declare function _internal_gun2_get_magazine_reloadtime(): f32;

/**
 */
export function gun2_get_magazine_reloadtime(): f32 {
	return _internal_gun2_get_magazine_reloadtime();
}

// @ts-ignore
@external("protologic", "gun3_get_bearing")
declare function _internal_gun3_get_bearing(): f32;

/**
 */
export function gun3_get_bearing(): f32 {
	return _internal_gun3_get_bearing();
}

// @ts-ignore
@external("protologic", "gun3_get_elevation")
declare function _internal_gun3_get_elevation(): f32;

/**
 */
export function gun3_get_elevation(): f32 {
	return _internal_gun3_get_elevation();
}

// @ts-ignore
@external("protologic", "gun3_get_refiretime")
declare function _internal_gun3_get_refiretime(): f32;

/**
 */
export function gun3_get_refiretime(): f32 {
	return _internal_gun3_get_refiretime();
}

// @ts-ignore
@external("protologic", "gun3_get_magazine_capacity")
declare function _internal_gun3_get_magazine_capacity(): i32;

/**
 */
export function gun3_get_magazine_capacity(): i32 {
	return _internal_gun3_get_magazine_capacity();
}

// @ts-ignore
@external("protologic", "gun3_get_magazine_remaining")
declare function _internal_gun3_get_magazine_remaining(): i32;

/**
 */
export function gun3_get_magazine_remaining(): i32 {
	return _internal_gun3_get_magazine_remaining();
}

// @ts-ignore
@external("protologic", "gun3_get_magazine_type")
declare function _internal_gun3_get_magazine_type(): i32;

/**
 */
export function gun3_get_magazine_type(): i32 {
	return _internal_gun3_get_magazine_type();
}

// @ts-ignore
@external("protologic", "gun3_get_magazine_reloadtime")
declare function _internal_gun3_get_magazine_reloadtime(): f32;

/**
 */
export function gun3_get_magazine_reloadtime(): f32 {
	return _internal_gun3_get_magazine_reloadtime();
}

