"""
Hydrogen atom quantum model.

This module provides analytical hydrogenic energy levels and
wavefunction probability-density calculations for visualization.
"""

from __future__ import annotations

from math import factorial, pi, sqrt
from typing import Dict

import numpy as np
from scipy.special import genlaguerre, sph_harm_y


# Physical constants
BOHR_RADIUS = 5.29177210903e-11  # meters
RYDBERG_ENERGY_EV = 13.605693122994  # eV


def validate_quantum_numbers(n: int, l: int, m: int) -> None:
    """Validate hydrogen quantum numbers."""

    if n < 1:
        raise ValueError("Principal quantum number n must be >= 1.")

    if l < 0 or l >= n:
        raise ValueError("Angular momentum quantum number l must satisfy 0 <= l < n.")

    if abs(m) > l:
        raise ValueError("Magnetic quantum number m must satisfy -l <= m <= l.")


def orbital_name(n: int, l: int, m: int) -> str:
    """Return a human-readable orbital name."""

    labels = {
        0: "s",
        1: "p",
        2: "d",
        3: "f",
    }

    angular_label = labels.get(l, f"l={l}")

    if l == 0:
        return f"{n}{angular_label}"

    return f"{n}{angular_label}, m={m}"


def energy_level(n: int) -> float:
    """
    Calculate the hydrogen energy level in electron volts.

    E_n = -13.605693 eV / n^2
    """

    if n < 1:
        raise ValueError("n must be >= 1.")

    return -RYDBERG_ENERGY_EV / (n**2)


def radial_wavefunction(n: int, l: int, r: np.ndarray) -> np.ndarray:
    """
    Calculate the normalized radial hydrogen wavefunction R_nl(r).

    r is expressed in units of the Bohr radius.
    """

    validate_quantum_numbers(n, l, 0)

    rho = 2.0 * r / n

    normalization = np.sqrt(
        (2.0 / n) ** 3
        * factorial(n - l - 1)
        / (2.0 * n * factorial(n + l))
    )

    laguerre = genlaguerre(n - l - 1, 2 * l + 1)(rho)

    return (
        normalization
        * np.exp(-rho / 2.0)
        * rho**l
        * laguerre
    )


def angular_wavefunction(l: int, m: int, theta: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """
    Calculate the spherical-harmonic angular wavefunction.

    theta: polar angle [0, pi]
    phi: azimuthal angle [0, 2*pi]
    """

    if abs(m) > l or l < 0:
        raise ValueError("Invalid angular quantum numbers.")

    # scipy.special.sph_harm_y uses (n, m, theta, phi), where
    # theta is the polar angle and phi is the azimuthal angle.
    return sph_harm_y(l, m, theta, phi)


def probability_density(
    n: int,
    l: int,
    m: int,
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
) -> np.ndarray:
    """
    Calculate the hydrogen probability density |psi|^2 on Cartesian points.

    x, y, z are expressed in units of the Bohr radius.
    """

    validate_quantum_numbers(n, l, m)

    r = np.sqrt(x**2 + y**2 + z**2)

    # Avoid division by zero at the origin.
    safe_r = np.where(r == 0, 1e-15, r)

    theta = np.arccos(np.clip(z / safe_r, -1.0, 1.0))
    phi = np.mod(np.arctan2(y, x), 2.0 * pi)

    radial = radial_wavefunction(n, l, r)
    angular = angular_wavefunction(l, m, theta, phi)

    psi = radial * angular

    return np.abs(psi) ** 2


def generate_probability_cloud(
    n: int,
    l: int,
    m: int,
    grid_size: int = 35,
    extent: float = 12.0,
    threshold: float = 0.02,
) -> Dict[str, list]:
    """
    Generate points representing the hydrogen orbital probability cloud.

    The spatial coordinates are expressed in Bohr radii.

    Only points whose normalized probability density exceeds the
    requested threshold are returned.
    """

    validate_quantum_numbers(n, l, m)

    if grid_size < 10:
        raise ValueError("grid_size must be at least 10.")

    if extent <= 0:
        raise ValueError("extent must be positive.")

    if not 0 < threshold < 1:
        raise ValueError("threshold must be between 0 and 1.")

    axis = np.linspace(-extent, extent, grid_size)

    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")

    density = probability_density(n, l, m, x, y, z)

    max_density = float(np.max(density))

    if max_density == 0:
        return {
            "x": [],
            "y": [],
            "z": [],
            "density": [],
        }

    normalized_density = density / max_density

    mask = normalized_density >= threshold

    return {
        "x": x[mask].astype(float).tolist(),
        "y": y[mask].astype(float).tolist(),
        "z": z[mask].astype(float).tolist(),
        "density": normalized_density[mask].astype(float).tolist(),
    }


def describe_state(n: int, l: int, m: int) -> Dict[str, object]:
    """Return basic information about a hydrogen quantum state."""

    validate_quantum_numbers(n, l, m)

    return {
        "n": n,
        "l": l,
        "m": m,
        "orbital": orbital_name(n, l, m),
        "energy_ev": energy_level(n),
        "bohr_radius_m": BOHR_RADIUS,
    }

def generate_cross_section(
    n: int,
    l: int,
    m: int,
    grid_size: int = 80,
    extent: float = 12.0,
) -> Dict[str, list]:
    """
    Generate a y=0 cross-section of the hydrogen probability density.

    The resulting x-z plane shows |psi(x, 0, z)|^2.
    """

    validate_quantum_numbers(n, l, m)

    if grid_size < 20:
        raise ValueError("grid_size must be at least 20.")

    if extent <= 0:
        raise ValueError("extent must be positive.")

    axis = np.linspace(-extent, extent, grid_size)

    x, z = np.meshgrid(axis, axis, indexing="ij")
    y = np.zeros_like(x)

    density = probability_density(n, l, m, x, y, z)

    max_density = float(np.max(density))

    if max_density == 0:
        return {
            "x": [],
            "z": [],
            "density": [],
        }

    normalized_density = density / max_density

    return {
        "x": x.flatten().astype(float).tolist(),
        "z": z.flatten().astype(float).tolist(),
        "density": normalized_density.flatten().astype(float).tolist(),
    }
